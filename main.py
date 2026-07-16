#!/usr/bin/env python3
"""AI-Team main entry point — interactive REPL."""

from communication import Communication


def main():
    model_key = "deepseek_v4_flash"
    role_name = "organizer"

    comm = Communication.get_or_create(model_key, role_name)
    print(f"Communication created with model: {comm.model['name']}")
    print(f"Role: {role_name}")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("Enter your message: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if user_input.lower() == "exit":
            break
        if not user_input:
            continue

        comm.append_user_message(user_input)
        comm.send()
        response = comm.last_response
        if response:
            print(f"\n{'='*60}")
            print(f"Response: {response}")
            print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
