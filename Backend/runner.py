from TrafficSimulation.model import TrafficModel
import argparse
import os


if __name__ == "__main__":
    env = os.environ
    parser = argparse.ArgumentParser(description='Run the traffic simulation.')
    parser.add_argument('--cycles', type=int, default=int(env.get("AGENT_CYCLE", 10)), help='Number of cycles in between agent spawners.')
    parser.add_argument('--post_step', type=int, default=int(env.get("POST_STEP", 100)), help='Number of steps in between posts.')
    parser.add_argument('--url', type=str, default=env.get("URL", None), help='Server URL for competition.')
    args = parser.parse_args()

    model = TrafficModel(agent_cycle=args.cycles,
                 post_cycle=args.post_step,
                 self_url=args.url)
    
    print("Model Initialized")

    while model.running:
        model.step()
        print("Model updated.", "Current Step:", model.num_steps)


    print("Simulation ended.")