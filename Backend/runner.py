from TrafficSimulation.model import TrafficModel
import argparse
import os


if __name__ == "__main__":
    env = os.environ
    parser = argparse.ArgumentParser(description='Run the traffic simulation.')
    parser.add_argument('--cycles', type=int, default=int(env.get("AGENT_CYCLE", 10)), help='Number of cycles in between agent spawners.')
    parser.add_argument('--post_step', type=int, default=int(env.get("POST_STEP", 100)), help='Number of steps in between posts.')
    parser.add_argument('--url', type=str, default=env.get("URL", None), help='Server URL for competition.')
    parser.add_argument('--log', type=str, default=env.get("LOG", None), help='File to log results to.')
    parser.add_argument('--limit', type=int, default=int(env.get("LIMIT", 1000)), help='Number of steps to run.')
    args = parser.parse_args()

    f = None

    if args.log is not None:
        f = open(f'{os.path.dirname(__file__)}/{args.log}', "w")
        f.write("step arrivals\n")
        f.flush()

    model = TrafficModel(agent_cycle=args.cycles,
                         post_cycle=args.post_step,
                         self_url=args.url,
                         limit=args.limit)
    
    print("Model Initialized")

    while model.running:
        model.step()
        print("Model updated.", "Current Step:", model.num_steps)
        if f is not None:
            f.write(f"{model.num_steps} {model.num_arrivals}\n")
            f.flush()

    if f is not None: f.close()
    print("Simulation ended.")