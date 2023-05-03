# Rocket CLI Tool

Rocket is a command-line interface tool for managing SSH connections. It simplifies the process of adding, launching,
and deleting connections.

## Installation

1. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the required packages:

```bash
2. pip install -r requirements.txt
```

3. Make the `main.py` file executable:

```bash
chmod +x main.py
```

4. Move and rename the `main.py` file to `/usr/local/bin/rocket`:

```bash
sudo mv main.py /usr/local/bin/rocket
```

Now, you can run the Rocket CLI tool by simply typing `rocket` in the terminal.

## Usage

1. Set the default username:

```bash
rocket install
```

2. Add a connection:

```bash
 rocket add --username <username> --host <host> [--nickname <nickname>] [--through-proxy]
 ```

3. Add a proxy:

```bash 
rocket add-proxy --username <username> --host <host> [--nickname <nickname>]
```

4. Launch a connection:

```bash
rocket launch [<nickname>]
```

5. Delete all connections and configuration:

```bash 
rocket delete
```

## Unit Tests

Run the unit tests with:

```bash
python -m unittest test_rocket.py
```

With these changes, users will be able to run the Rocket CLI tool directly from their terminal by typing rocket followed
by the desired subcommand.




