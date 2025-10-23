Why It’s Important to save environment variables using dotenv?

- Security – You don’t accidentally expose secrets (API keys, passwords, tokens) if you share your code publicly (g., on GitHub).
- Flexibility – You can easily switch environments (development, testing, production) by using different .env files.
- Portability – Other people can run your project by simply setting up their own .env file — no code changes needed.
- Clean Code – Your Python scripts stay focused on logic, not configuration.

  In big organisations there are a lot of environment variables..be it database variables or api keys.. all these needs to be loaded in a standard form
  as not 1 sec of downtime is acceptable due to code failure.
  To ensure flexibility of changing environments, It is necessary to maintain a seperate file of environment. 
