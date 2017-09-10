from itertools import permutations

class Event:
    def __init__(self, name="event", text="event text", persons=1,conditions=[], effects=[], choices=[], choices_result_text=[], choices_effects=[]):
        self.name = name
        self.text = text
        self.conditions = conditions
        self.effects = effects

        self.graph = None
        self.target_persons = None

        assert persons >= 1
        self.persons = persons

        assert len(choices) == len(choices_result_text) == len(choices_effects)
        self.choices = choices
        self.choices_result_text = choices_result_text
        self.choices_effects = choices_effects

    def __repr__(self):
        return "{}".format(
            self.name)

    def set_targets(self, graph, persons):
        # graph, persons should meet conditions
        assert(len(persons) == self.persons)
        self.graph = graph
        self.target_persons = persons

    def conditions_check(self, graph, persons):
        assert(len(persons) == self.persons)
        for condition in self.conditions:
            if condition(graph, persons) == False: 
                return False
        return True

    def apply_effects(self):
        assert self.graph != None and self.target_persons != None
        for effect in self.effects:
            effect(self.graph, self.target_persons)

    def apply_choice_effects(self, choice):
        if choice == -1:
            return
        assert self.graph != None and self.target_persons != None
        assert choice >=0 and choice <= len(self.choices)
        for choices_effect in self.choices_effects[choice]:
            choices_effect(self.graph, self.target_persons)

    def get_text(self, selected_choice=-1):
        text = self.text + "\n"
        for i, choice in enumerate(self.choices):
            if i == selected_choice:
                text += "{}. {}\t\t<< selected\n".format(i, choice)
            else:
                text += "{}. {}\n".format(i, choice)

        if selected_choice != -1:
            assert selected_choice >=0 and selected_choice <= len(self.choices)
            text += ">> {}\n".format(self.choices_result_text[selected_choice])

        return text


def get_valid_persons(graph, event, fixed_persons=None):
    persons = graph.graph.nodes()
    valid = permutations(persons, event.persons)
    if fixed_persons != None:
        valid = [x for x in valid if False not in [fixed_persons[i] == None or p == fixed_persons[i] for i,p in enumerate(x)]]
    valid = [x for x in valid if event.conditions_check(graph, x)]
    return valid

def get_all_valid_events(graph):
    valid = []
    for event in events:
        vals = get_valid_persons(graph, event)
        for val in vals:
            valid.append([event, val])
    return valid

def get_valid_events_per_person(graph, all_valid_events=None):
    if all_valid_events == None:
        all_valid_events = get_all_valid_events(graph)
    valid_events_per_person = {}
    for [event, persons] in all_valid_events:
        p = None
        if len(persons) > 0:
            p = persons[0]
        if valid_events_per_person.get(p) == None:
            valid_events_per_person[p] = []
        valid_events_per_person[p].append([event, persons])
    return valid_events_per_person

def set_interacted(graph, person0, person1):
    graph.graph.add_edge(*(person0, person1))
    graph.graph[person0][person1]["interacted"] = True

def add_sentiment(graph, person0, person1, value):
    graph.graph.add_edge(*(person0, person1))
    if "sentiment" not in graph.graph[person0][person1]:
        graph.graph[person0][person1]["sentiment"] = 0    
    graph.graph[person0][person1]["sentiment"] += value

def set_location(graph, person, location):
    person.location = location

events = [
    Event(name="Maybe talk",
            text="Your eyes meet {}.",
            persons=2,
            conditions=[
              lambda graph, persons: persons[0].location == persons[1].location
            ],
            effects=[
              lambda graph, persons: set_interacted(graph, persons[0], persons[1])
            ],
            choices=[
              "Talk",
              "Ignore"
            ],
            choices_result_text=[
              "Hello!",
              "You walk away."
            ],
            choices_effects=[
                [
                    lambda graph, persons: add_sentiment(graph, persons[0], persons[1], 1)
                ],
                [
                    lambda graph, persons: add_sentiment(graph, persons[0], persons[1], -0.1)
                ]         
            ]
        ),
    Event(name="Maybe go for tea",
            text="You see {}. Invite {} for tea?",
            persons=2,
            conditions=[
              lambda graph, persons: persons[0].location == persons[1].location,
              lambda graph, persons: persons[1] in graph.graph[persons[0]] and graph.graph[persons[0]][persons[1]]['sentiment'] >= 3
            ],
            effects=[
              lambda graph, persons: set_interacted(graph, persons[0], persons[1])
            ],
            choices=[
              "Yes",
              "No"
            ],
            choices_result_text=[
              "Tea was great!",
              "Maybe next time."
            ],
            choices_effects=[
                [
                    lambda graph, persons: add_sentiment(graph, persons[0], persons[1], 10)
                ],
                [
                    lambda graph, persons: add_sentiment(graph, persons[0], persons[1], -0.1)
                ]         
            ]
        ),
    Event(name="Goto Class A",
            text="You walk to class A",
            persons=1,
            conditions=[
              lambda graph, persons: persons[0].location != "Class A"
            ],
            effects=[
              lambda graph, persons: set_location(graph, persons[0], "Class A")
            ]
        ),
    Event(name="Goto Class B",
            text="You walk to class B",
            persons=1,
            conditions=[
              lambda graph, persons: persons[0].location != "Class B"
            ],
            effects=[
              lambda graph, persons: set_location(graph, persons[0], "Class B")
            ]
        )


]


