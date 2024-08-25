import os

from openai import OpenAI

from gridiot.schemas import BaseballQuery


ai_client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


def generate_query(user_query: str) -> BaseballQuery:
    system_prompt = """
**Task:** You are an AI designed to parse baseball-related queries into structured data. Your output must conform to a predefined schema, which you have been supplied separately. You will be given a natural language query, and your job is to convert it into the corresponding JSON object based on the schema.

**Instructions:**

1. Parse the natural language query into the appropriate JSON structure according to the schema provided.
2. Identify and convert informal team names to the correct team codes as per the guidelines supplied.
3. Distribute conditions and group them logically according to the intent of the query. Use "AND" or "OR" operators to appropriately group conditions.

**Example Queries:**

- *Query*: "Nationals and Cubs with 3 or more WAR."
- *JSON Output*:
  ```json
  {
    "root": {
      "operator": "AND",
      "criteria": [
        {
          "operator": "OR",
          "criteria": [
            {
              "type": "team",
              "value": {
                "team": "WSN"
              }
            },
            {
              "type": "team",
              "value": {
                "team": "CHN"
              }
            }
          ]
        },
        {
          "type": "stat",
          "value": {
            "stat": "WAR",
            "operator": ">=",
            "value": 3.0
          }
        }
      ]
    }
  }
  ```

- *Query*: "White Sox players who played with the Cubs."
- *JSON Output*:
  ```json
  {
    "root": {
      "operator": "AND",
      "criteria": [
        {
          "type": "team",
          "value": {
            "team": "CHW"
          }
        },
        {
          "type": "team",
          "value": {
            "team": "CHC"
          }
        }
      ]
    }
  }
  ```

- *Query*: "Cubs players who won Rookie of the Year."
- *JSON Output*:
  ```json
  {
    "root": {
      "operator": "AND",
      "criteria": [
        {
          "type": "team",
          "value": {
            "team": "CHC"
          }
        },
        {
          "type": "award",
          "value": {
            "award": "Rookie of the Year"
          }
        }
      ]
    }
  }
  ```

- *Query*: "Players who played for the Reds and Nationals with 3 or more WAR."
- *JSON Output*:
  ```json
  {
    "root": {
      "operator": "AND",
      "criteria": [
        {
          "operator": "OR",
          "criteria": [
            {
              "type": "team",
              "value": {
                "team": "CIN"
              }
            },
            {
              "type": "team",
              "value": {
                "team": "WSN"
              }
            }
          ]
        },
        {
          "type": "stat",
          "value": {
            "stat": "WAR",
            "operator": ">=",
            "value": 3.0
          }
        }
      ]
    }
  }
  ```

- *Query*: "Players who played center field and won a Silver Slugger."
- *JSON Output*:
  ```json
  {
    "root": {
      "operator": "AND",
      "criteria": [
        {
          "type": "position",
          "value": {
            "position": "CF"
          }
        },
        {
          "type": "award",
          "value": {
            "award": "Silver Slugger"
          }
        }
      ]
    }
  }
  ```

**Your turn:** Here’s the natural language query. Parse it into the structured format.

Convert references to cities and informal nicknames into appropriate short team names.
Use this list of awards to translate names: {AWARDS}
"""

    completion = ai_client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Query: {user_query}"},
        ],
        response_format=BaseballQuery,
    )

    return completion.choices[0].message.parsed
