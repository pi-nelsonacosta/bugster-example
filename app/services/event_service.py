from collections import defaultdict
from app.schemas.event import EventInput, UserStory, PlaywrightTest
from typing import List
from app.db.repository.event_repository import (
    get_events_by_session_id,
    get_tests_by_story_id,
    store_events,
    get_stories_by_session_id,
    create_user_story,
    store_tests
)

class EventService:

    async def store_events(self, events: List[EventInput]):
        """Almacena una lista de eventos en la base de datos, agrupa en historias y genera tests."""
        try:
            # Guardar los eventos
            await store_events(events)
            print("Eventos almacenados correctamente.")

            # Agrupar eventos en historias de usuario
            stories = await self.group_events_into_stories(events)

            # Generar y almacenar los tests automáticamente para cada historia generada
            for story in stories:
                await self._generate_and_store_tests(story, events)

        except Exception as e:
            print(f"Error en store_events: {e}")
            raise e
    
    async def group_events_into_stories(self, events: List[EventInput]) -> List[UserStory]:
        """Agrupa eventos en historias de usuario basadas en el session_id y patrones de comportamiento."""

        grouped_events = defaultdict(list)

        # Agrupar eventos por session_id
        for event in events:
            session_id = event.properties.get("session_id")
            grouped_events[session_id].append(event)

        stories = []
        for session_id, session_events in grouped_events.items():
            session_events.sort(key=lambda e: e.properties.get("timestamp"))

            journey_id = session_events[0].properties.get("journey_id")
            description = f"Historia generada automáticamente para sesión {session_id}"

            # Crear una historia de usuario
            story = await create_user_story(session_id, journey_id, description)
            stories.append(story)

        print(f"Historias generadas: {stories}")
        return stories    

    async def get_user_stories(self, session_id: str = None) -> List[UserStory]:
        """Obtiene historias de usuario filtradas por session_id."""
        try:
            print(f"Buscando historias con session_id: {session_id}")
            stories = await get_stories_by_session_id(session_id)
            print(f"Historias encontradas: {stories}")
            return stories
        except Exception as e:
            print(f"Error en get_user_stories: {e}")
            raise e
    
    async def get_tests_by_story_id(self, story_id: str) -> List[PlaywrightTest]:
        """Obtiene los tests almacenados por story_id."""
        try:
            print(f"Buscando tests para story_id: {story_id}")
            tests = await get_tests_by_story_id(story_id)
            print(f"Tests encontrados: {tests}")
            return tests
        except Exception as e:
            print(f"Error en get_tests_by_story_id: {e}")
            raise e    

    async def _generate_and_store_tests(self, story: UserStory, events: List[EventInput]):
        """Genera y almacena tests basados en una historia y una lista de eventos."""
        try:
            test_steps = []
            screenshot_counter = 1  # Contador para capturas de pantalla

            # Función auxiliar para agregar un paso de click
            def add_click_step(selector):
                nonlocal screenshot_counter
                test_steps.append(f'page.wait_for_selector("{selector}")')
                test_steps.append(f'assert page.query_selector("{selector}") is not None, "Selector \'{selector}\' no encontrado en la página"')
                test_steps.append(f'page.click("{selector}")')
                test_steps.append(f'page.screenshot(path="screenshot_click_{screenshot_counter}.png")')
                screenshot_counter += 1

            # Función auxiliar para agregar un paso de input
            def add_input_step(selector, value):
                nonlocal screenshot_counter
                test_steps.append(f'page.wait_for_selector("{selector}")')
                test_steps.append(f'assert page.query_selector("{selector}") is not None, "Selector \'{selector}\' no encontrado en la página"')
                test_steps.append(f'page.fill("{selector}", "{value}")')
                test_steps.append(f'page.screenshot(path="screenshot_input_{screenshot_counter}.png")')
                screenshot_counter += 1

            # Función auxiliar para agregar un paso de navegación
            def add_navigation_step(url):
                nonlocal screenshot_counter
                test_steps.append(f'page.goto("{url}")')
                test_steps.append(f'assert page.url == "{url}", "No se navegó correctamente a la URL \'{url}\'"')
                test_steps.append(f'page.screenshot(path="screenshot_navigation_{screenshot_counter}.png")')
                screenshot_counter += 1

            # Procesar los eventos y generar los pasos correspondientes
            for event in events:
                event_type = event.properties.get("eventType")
                attributes = event.properties.get("elementAttributes", {})

                # Priorizar selectores más robustos: id > data-testid > class
                selector = attributes.get("id") or attributes.get("data-testid") or attributes.get("class")

                if event_type == "click" and selector:
                    add_click_step(selector)

                elif event_type == "input" and selector:
                    value = event.properties.get("elementText", "")
                    add_input_step(selector, value)

                elif event_type == "navigation":
                    url = event.properties.get("$current_url", "")
                    if url:
                        add_navigation_step(url)

            # Generar el script solo si hay pasos válidos
            if test_steps:
                test_script = f"""from playwright.sync_api import sync_playwright, TimeoutError

def test_user_journey_{story.session_id.replace('-', '_')}():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
{chr(10).join(f'            {step}' for step in test_steps)}
        except TimeoutError as e:
            print(f"Error: {{e}}")
        finally:
            browser.close()
"""


                # Crear el test Playwright
                test = PlaywrightTest(story_id=str(story.id), test_script=test_script)

                # Guardar el test en la base de datos
                await store_tests([test])
                print(f"Test generado y almacenado: {test}")

                return [test]
            else:
                print("No se generaron pasos para el test.")
                return []

        except Exception as e:
            print(f"Error en _generate_and_store_tests: {e}")
            raise e



