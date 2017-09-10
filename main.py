from Event import Event
from Event import events, get_valid_persons, get_all_valid_events, get_valid_events_per_person
from SocialGraph import SocialGraph, Person

import json
import random

random.seed(1234567890)

def main():
    social_graph = SocialGraph("Test Scenario")
    print(social_graph.scenario_name)


    # player = Person(name="Player", location="Class A")
    a = Person(name="A", location="Class A")
    b = Person(name="B", location="Class A")
    c = Person(name="C", location="Class B")
    # d = Person(name="D", location="Class B")
    # e = Person(name="E", location="Class B")

    # social_graph.add_persons([player, a, b, c, d, e])

    social_graph.add_persons([a, b, c])

    # social_graph.update_relation(a, b, {"sentiment": 1})
    # print(social_graph)

    for timestep in range(15):
        social_graph.timestep = timestep


        all_valid_events = get_all_valid_events(social_graph)
        valid_events_per_person = get_valid_events_per_person(social_graph, all_valid_events)
        # print("\n".join((str(k) + ": " + str(v) for k,v in valid_events_per_person.items())))

        # for each player
        for (person,valid_events) in valid_events_per_person.items():
            # Pick a random event
            event, persons = random.choice(valid_events)
            event.set_targets(social_graph, persons)
            
            # Pick a random choice
            choice = -1
            if len(event.choices) > 0:
                choice = random.choice(range(len(event.choices)))
            
            # Apply effects
            event.apply_effects()

            # Print text
            # if person == player:
            print("[{}]\n{}".format(person, event.get_text(choice)))

            # Apply picked choice effects
            event.apply_choice_effects(choice)



        print("=========={}==========".format(timestep))
        print(social_graph)
        print("=========={}==========".format(timestep))


def loop():
    pass

    #initialize

    # for each timestep
        # for each person
            # find all events that meet conditions, with N persons involved
            # pick a random valid event
            # execute event
                # apply effects
                # wait for choice, or pick a random choice
                # apply choice effects

        # IDEA: fixed events every timestep
        # IDEA: immediate events - trigger once conditions are fufilled




if __name__ == '__main__':
    main()