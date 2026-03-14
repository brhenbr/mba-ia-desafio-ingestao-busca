import sys
from search import search_prompt

def main():
    """
    Main CLI loop for interaction with the PDF assistant.
    Handles user inputs and graceful shutdowns.
    """
    print("[*] Initializing PDF AI Assistant...")
    
    # Retrieve the configured chain from search.py
    chain = search_prompt()

    if not chain:
        print("[!] System initialization failed. Terminating process.")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("PDF ASSISTANT READY - Type your question or 'exit' to quit")
    print("="*60)

    while True:
        try:
            # Capturing user input and cleaning whitespace
            query = input("\nQuestion: ").strip()

            if not query:
                continue

            # Termination signals
            if query.lower() in ['exit', 'quit', 'sair', 'stop']:
                print("[*] Shutting down assistant. Goodbye!")
                break

            # Invoking the chain and displaying the result
            print("[*] Retrieving context and generating answer...")
            response = chain.invoke(query)
            print(f"\nANSWER: {response}")

        except KeyboardInterrupt:
            # Handling Ctrl+C 
            print("\n\n[*] Keyboard interrupt detected. Exiting cleanly...")
            break
        except Exception as e:
            # Non-fatal error handling to keep the chat loop alive
            print(f"\n[!] An error occurred during processing: {e}")
            print("[*] You may try another question.")

if __name__ == "__main__":
    main()