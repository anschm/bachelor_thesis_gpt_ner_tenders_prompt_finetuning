from prompt_strategy import PromptStrategy


class PromptBuilder:
    """
    Builds prompts for entity recognition tasks in tender documents. It formats
    the output using predefined templates and supports zero-shot and one-shot
    prompt strategies.

    Attributes:
        task_description_template (str): Template describing the task for entity recognition.
        entity_definitions_template (str): Template defining the entities to recognize.
        task_emphasis_template (str): Template emphasizing important aspects for the task.
        examples_template (str): Template used for formatting examples.
        task_template (str): Template for the expected output format.
        promt_template (str): Base template combining all others to structure the final prompt.
    """

    task_description_template = '''##Aufgabenbeschreibung##
Du sollst Entitäten in dieser öffentlichen Ausschreibung erkennen:'''

    entity_definitions_template = '''##Definitionen der Entitäten##
Folgende Entitäten sollst du erkennen:
1. Veröffentlichungsdatum (Synonyme: Datum der Veröffentlichung, Bekanntmachung): kann in verschiedenen Formaten vorliegen (bspw. 23.01.2025, 23. Januar 2025).
2. Erfüllungsort (Synonyme: Ort der Ausführung, Leistungsort, Ort der Leistungserbringung): hierbei kann es sich um eine vollständige Adresse mit Straße, Hausnummer, Postleitzahl und Stadt, als auch um eine einfache Ortsangabe in Form einer Stadt handeln. 
3. Vergabestelle (Synonyme: Auftraggeber, Beschaffer): die liegt häufig als verschachteltes Objekt vor (bspw. "Bundesministerium für Verkehr und digitale Infrastruktur").
4. Geschäftszeichen (Synonyme: Vergabenummer, Identifikationsnummer, Vergabenr., Projektnummer, Interne Kennung): setzt sich typischerweise aus der Behörde oder Institution, dem Jahr der Veröffentlichung, einer fortlaufenden Ausschreibungsnummer und gegebenenfalls der Art der Ausschreibung zusammen (z. B. 0362/25-B-Ö-21).'''

    task_emphasis_template = '''##Aufgabenschwerpunkte##
Bevor du die Lösung abgibst, überprüfe bei jeder Entität, ob du sie wirklich 
richtig und vollständig identifiziert hast. Entitäten sind nur dann richtig erkannt, 
wenn sie vollständig und korrekt erkannt wurden. Entitäten können diskontinuierlich oder geschachtelte Objekte, 
wie bspw. "Bundesministreium für Verkehr und digitale Infrastruktur", sein.'''

    examples_template = '''##Übungsbeispiel##
{0}'''

    task_template = '''##Ausgabeindikator##
Gebe den Auszug aus der Ausschreibung vollständig zurück. Markiere die 
gefundenen Entitäten wie folgt: die Entität wird mit Prefix @@ und dem Suffix **
gekennzeichnet. Schreibe in Klammern die Art der Entität dahinter (Veröffentlichunsdatum, Erfüllungsort, Vergabestelle oder Geschäftszeichen).'''

    promt_template = '''{task_description}
{entity_definitions}
{task_emphasis}
{examples}
{task}
{tender_html}
'''

    def build_zero_shot(self, tender_html: str) -> str:
        """
        Constructs a zero-shot prompt using the provided tender HTML content.

        Args:
            tender_html (str): The HTML content of the tender document.

        Returns:
            str: A formatted prompt for zero-shot entity recognition.
        """
        return self.promt_template.format(
            task_description=self.task_description_template,
            entity_definitions=self.entity_definitions_template,
            task_emphasis=self.task_emphasis_template,
            examples="",
            task=self.task_template,
            tender_html=tender_html
        )

    def build_one_shot(self, tender_html: str, example: str) -> str:
        """
        Constructs a one-shot prompt using the provided tender HTML content
        and an example.

        Args:
            tender_html (str): The HTML content of the tender document.
            example (str): Example to include in the prompt for guidance.

        Returns:
            str: A formatted prompt for one-shot entity recognition.

        Raises:
            ValueError: If no example is provided for a one-shot strategy.
        """

        if not example:
            raise ValueError("No example provided for one shot prompt strategy")
        return self.promt_template.format(
            task_description=self.task_description_template,
            entity_definitions=self.entity_definitions_template,
            task_emphasis=self.task_emphasis_template,
            examples=self.examples_template.format(example),
            task=self.task_template,
            tender_html=tender_html
        )

    def build(self, prompt_strategy: PromptStrategy, tender_html: str, examples: list[str]) -> str:
        """
        Constructs a prompt based on the specified strategy, tender content,
        and examples.

        Args:
            prompt_strategy (PromptStrategy): The strategy to use for building the prompt
                (e.g., zero-shot or one-shot).
            tender_html (str): The HTML content of the tender document.
            examples (list[str]): A list of examples for the prompt.

        Returns:
            str: A formatted prompt based on the chosen strategy.

        Raises:
            ValueError: If the incorrect number of examples is provided for the strategy
                or if an unknown strategy is specified.
        """
        match prompt_strategy:
            case PromptStrategy.ZERO_SHOT:
                return self.build_zero_shot(tender_html)
            case PromptStrategy.ONE_SHOT:
                if len(examples) < 1:
                    raise ValueError("No examples provided for one shot prompt strategy")
                return self.build_one_shot(tender_html, examples[0])
        raise ValueError("Unknown prompt strategy")
