import matplotlib.pyplot as plt


class Citizen:
    def __init__(self, name, nic, age, state):
        self.name = name
        self.nic = nic
        self.age = age
        self.state = state

class Candidate(Citizen):
    def __init__(self, name, nic, age, state, party):
        super().__init__(name, nic, age, state)
        self.party = party

class ElectionSystem:
    def __init__(self):
        self.citizens = []
        self.candidates = {}
        self.votes = {}

    def add_citizen(self, name, nic, age, state):
        citizen = Citizen(name, nic, age, state)
        self.citizens.append(citizen)

    def add_candidate(self, name, nic, age, state, party):
        if state not in self.candidates:
            self.candidates[state] = []
        candidate = Candidate(name, nic, age, state, party)
        self.candidates[state].append(candidate)

    def vote(self):
        nic = input("Enter your NIC: ")
        citizen = next((c for c in self.citizens if c.nic == nic), None)
        if not citizen:
            print("Citizen not found!")
            return

        if citizen.age < 18:
            print("Only citizens above the age of 18 can vote.")
            return

        if citizen.nic in self.votes:
            print("Citizen has already voted.")
            return

        state_candidates = self.candidates.get(citizen.state, [])
        print("Available candidates:")
        for i, candidate in enumerate(state_candidates):
            print(f"{i+1}. {candidate.name} ({candidate.party})")

        candidate_nics = []
        votes_left = 3
        while votes_left > 0:
            candidate_nic = input(f"Enter the NIC of the candidate you want to vote for ({votes_left} vote(s) left) (or 'done' to finish): ")
            if candidate_nic == "done":
                break
            candidate = next((c for c in state_candidates if c.nic == candidate_nic), None)
            if not candidate:
                print("Invalid candidate NIC.")
                continue
            if candidate_nic in candidate_nics:
                print("You have already voted for this candidate.")
                continue
            candidate_nics.append(candidate_nic)
            votes_left -= 1

        if not candidate_nics:
            print("No votes recorded.")
            return

        self.votes[citizen.nic] = candidate_nics
        print(f"Vote successfully recorded for citizen {citizen.name}.")

    def calculate_votes(self):
        results = {}
        for state, candidates in self.candidates.items():
            state_votes = {}
            for candidate in candidates:
                state_votes[candidate.name] = 0
            results[state] = state_votes

        for candidate_nics in self.votes.values():
            for state, candidates in self.candidates.items():
                for candidate_nic in candidate_nics:
                    candidate = next((c for c in candidates if c.nic == candidate_nic), None)
                    if candidate:
                        results[state][candidate.name] += 1

        return results

    def display_results(self):
        results = self.calculate_votes()
        for state, state_votes in results.items():
            print(f"--- Results for {state} ---")
            for candidate, votes in state_votes.items():
                print(f"{candidate}: {votes} votes")
            print()

        # Create a bar chart
        fig, ax = plt.subplots()
        for i, (state, state_votes) in enumerate(results.items()):
            candidates = list(state_votes.keys())
            votes = list(state_votes.values())
            x_pos = [i for i, _ in enumerate(candidates)]
            ax.bar(x_pos, votes, align='center', alpha=0.5)
            ax.set_xlabel('Candidates')
            ax.set_ylabel('Votes')
            ax.set_title(f'Election Results - {state}')
            ax.set_xticks(x_pos)
            ax.set_xticklabels(candidates)
            plt.show()


# Example usage

# Create an instance of the ElectionSystem
election_system = ElectionSystem()

# Add citizens
election_system.add_citizen("John Doe", "123456789", 25, "California")
election_system.add_citizen("Jane Smith", "987654321", 30, "California")
election_system.add_citizen("Alice Johnson", "456789123", 20, "Texas")
election_system.add_citizen("Bob Brown", "789123456", 22, "Texas")

# Add candidates
election_system.add_candidate("Candidate A", "111111111", 35, "California", "Party 1")
election_system.add_candidate("Candidate B", "222222222", 40, "California", "Party 2")
election_system.add_candidate("Candidate C", "333333333", 30, "Texas", "Party 1")
election_system.add_candidate("Candidate D", "444444444", 28, "Texas", "Party 2")

# Cast votes
election_system.vote()
election_system.vote()
election_system.vote()
election_system.vote()

# Display the results
election_system.display_results()