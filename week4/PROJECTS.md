# Week 4 projects: an LLM app, one per person

Each person builds **one small LLM app** end to end. Your project is listed below. Present it on **Tuesday 3 November** (Tuesday of Week 5).

## What every project must have

| # | Requirement | What "done" looks like |
|---|---|---|
| 1 | **Prompt engineering** | At least **3 techniques** (from zero-shot, few-shot, role/system prompt, chain of thought), written as separate prompt functions |
| 2 | **Structured output + Pydantic** | The LLM returns JSON that is validated with a Pydantic model, with one retry on a `ValidationError` |
| 3 | **Accuracy comparison** | A labelled set of **at least 20 examples** you check by hand; a table of field-level accuracy per prompting technique; say which one you chose and why |
| 4 | **LLM as a judge** | A rubric-based judge that scores the app's free-text output (1–5 + reason, validated with Pydantic); check it against your own scores on 10 examples and report the agreement |
| 5 | **FastAPI backend** | At least `GET /health` and one `POST` endpoint for the main feature, with Pydantic request/response models and sensible status codes (422 / 400 / 503) |
| 6 | **Streamlit frontend** | A page that calls your FastAPI backend (never the LLM directly) and shows the structured result and the judge's score |
| 7 | **Docker** | A `Dockerfile` for the backend and the frontend, and a `docker-compose.yml` so `docker compose up --build` starts the whole app |
| 8 | **Secrets and repo** | Azure OpenAI settings in `.env` (never committed), a `.env.example`, and a README with how to run it and your accuracy table |

**No project needs real data.** Each needs **at least 20 labelled examples**: made-up (synthetic) data is fine, and a public dataset is optional. Every example is one row: the `input` text and the `expected` structured answer, which you label by hand and use for the accuracy table.

Use [Notebook 2](02_prompt_engineering_simple.ipynb) for the prompting, Pydantic, accuracy and judge code, and the
[Streamlit + FastAPI + MLflow demo](https://github.com/samuelts96/streamlit-fastapi-mlflow) as the template for the
FastAPI / Streamlit / Docker Compose layout (you don't need MLflow).

**Suggested layout**

```
backend/     FastAPI app: prompts.py, schemas.py (Pydantic), judge.py, main.py, Dockerfile
frontend/    Streamlit app.py, Dockerfile
notebooks/   prompt comparison + judge calibration
data/        labelled examples (CSV/JSON)
docker-compose.yml
.env.example
README.md
```

Only use public or made-up data. **Never put real personal data into a prompt.**

---

## The projects

### Akinlolu Oyetakin · Job advert analyser
Paste a job advert; the app extracts `job_title`, `seniority` (junior / mid / senior), `required_skills` (list), `nice_to_have_skills`, `salary_min` / `salary_max` (or null) and `remote` (remote / hybrid / onsite), then writes 3 CV bullet suggestions that match the advert.
**Judge:** scores the CV bullets on relevance to the advert, specificity and honesty (no invented experience).
**Data:** at least 20 labelled examples; synthetic (written by you or generated) is fine. Optional public source: LinkedIn Job Postings (Kaggle).

Example row (the `input`, and the `expected` answer you label by hand):
```json
{
  "input": "Junior Data Analyst, Manchester (hybrid, 3 days in office). £28,000-£32,000. You'll need SQL, Excel and Power BI; Python is a plus. 0-2 years' experience.",
  "expected": {
    "job_title": "Data Analyst",
    "seniority": "junior",
    "required_skills": [
      "SQL",
      "Excel",
      "Power BI"
    ],
    "nice_to_have_skills": [
      "Python"
    ],
    "salary_min": 28000,
    "salary_max": 32000,
    "remote": "hybrid"
  }
}
```

### Dr. Janki Pal · Patient feedback triage (synthetic data)
Paste a piece of hospital patient feedback; the app extracts `department`, `issue_type` (clinical care / waiting time / staff attitude / facilities / communication / praise), `urgency` (low / medium / high) and `sentiment`, then drafts a reply from the patient experience team.
**Judge:** scores the reply on empathy, addressing every concern raised and making no clinical promises.
**Data:** at least 20 labelled examples; synthetic (written by you or generated) is fine. Synthetic only: never use real patient feedback.

Example row (the `input`, and the `expected` answer you label by hand):
```json
{
  "input": "I waited four hours in A&E with my son and nobody told us what was happening. The nurse who finally saw us was lovely though.",
  "expected": {
    "department": "Emergency (A&E)",
    "issue_type": "waiting time",
    "urgency": "medium",
    "sentiment": "mixed"
  }
}
```

### Saraswathi Lakshman · Recipe and allergen assistant
Paste a recipe; the app extracts `ingredients` (name + quantity), `allergens` (from the 14 major allergens), `diet` (vegan / vegetarian / none), `prep_minutes` and `difficulty`, then suggests one substitution that removes the main allergen.
**Judge:** scores the substitution on whether it actually removes the allergen and keeps the dish workable.
**Data:** at least 20 labelled examples; synthetic (written by you or generated) is fine. Optional public source: Food.com Recipes (Kaggle).

Example row (the `input`, and the `expected` answer you label by hand):
```json
{
  "input": "Pesto pasta: 200 g spaghetti, 50 g basil, 30 g pine nuts, 40 g parmesan, 2 cloves garlic, 80 ml olive oil. Blend, toss with pasta. 20 minutes.",
  "expected": {
    "ingredients": [
      {
        "name": "spaghetti",
        "quantity": "200 g"
      },
      {
        "name": "basil",
        "quantity": "50 g"
      },
      {
        "name": "pine nuts",
        "quantity": "30 g"
      },
      {
        "name": "parmesan",
        "quantity": "40 g"
      },
      {
        "name": "garlic",
        "quantity": "2 cloves"
      },
      {
        "name": "olive oil",
        "quantity": "80 ml"
      }
    ],
    "allergens": [
      "gluten",
      "milk"
    ],
    "diet": "vegetarian",
    "prep_minutes": 20,
    "difficulty": "easy"
  }
}
```

### Tejaswini Pandiri · Customer support ticket router
Paste a support email; the app extracts `category` (billing / technical / delivery / account / other), `priority` (low / medium / high), `product` and `customer_wants` (refund / fix / information / cancel), then drafts a first reply.
**Judge:** scores the reply on answering the actual question, tone and making no promises outside policy.
**Data:** at least 20 labelled examples; synthetic (written by you or generated) is fine. Optional public source: Customer Support Ticket Dataset (Kaggle).

Example row (the `input`, and the `expected` answer you label by hand):
```json
{
  "input": "I was charged twice for my March subscription to the Premium plan. Please send the extra £12.99 back to my card.",
  "expected": {
    "category": "billing",
    "priority": "medium",
    "product": "Premium plan",
    "customer_wants": "refund"
  }
}
```

### Egbierele Uku · Receipt and invoice extractor
Paste the text of a receipt or invoice; the app extracts `vendor`, `date` (ISO format), `currency`, `line_items` (description, quantity, price), `total` and `vat`, and Pydantic checks that the line items add up to the total. It then writes a one-line expense description.
**Judge:** scores whether the expense description is accurate and complete for the receipt.
**Data:** at least 20 labelled examples; synthetic (written by you or generated) is fine. Made-up receipts are fine (or your own with personal details removed).

Example row (the `input`, and the `expected` answer you label by hand):
```json
{
  "input": "BEAN & LEAF CAFE  14/10/2026\n2 x Flat white   3.40   6.80\n1 x Croissant    2.60   2.60\nTOTAL GBP 9.40  (VAT incl. 1.57)",
  "expected": {
    "vendor": "Bean & Leaf Cafe",
    "date": "2026-10-14",
    "currency": "GBP",
    "line_items": [
      {
        "description": "Flat white",
        "quantity": 2,
        "price": 3.4
      },
      {
        "description": "Croissant",
        "quantity": 1,
        "price": 2.6
      }
    ],
    "total": 9.4,
    "vat": 1.57
  }
}
```

### Mojeed Adekunbi Rafiu · News article summariser and classifier
Paste a news article; the app extracts `topic` (business / politics / sport / tech / entertainment), `people`, `organisations`, `locations` and `sentiment`, and writes a 3-bullet summary.
**Judge:** scores the summary on faithfulness (nothing that isn't in the article), coverage of the main points and brevity.
**Data:** at least 20 labelled examples; synthetic (written by you or generated) is fine. Optional public source: BBC News classification dataset (Kaggle / Hugging Face), or short articles you write.

Example row (the `input`, and the `expected` answer you label by hand):
```json
{
  "input": "Northfield Rovers manager Sam Okafor praised striker Leo Grant after his two goals secured a 2-1 win over Eastbridge City at Riverside Park on Sunday.",
  "expected": {
    "topic": "sport",
    "people": [
      "Sam Okafor",
      "Leo Grant"
    ],
    "organisations": [
      "Northfield Rovers",
      "Eastbridge City"
    ],
    "locations": [
      "Riverside Park"
    ],
    "sentiment": "positive"
  }
}
```

### Helena Lawrence · Product review insights
Paste a product review; the app extracts each `aspect` mentioned (quality / price / delivery / packaging / customer service) with its own sentiment, an overall `rating_guess` (1–5) and `would_recommend`, then writes a one-sentence summary for the product team.
**Judge:** scores the summary on accuracy to the review and usefulness to the product team.
**Data:** at least 20 labelled examples; synthetic (written by you or generated) is fine. Optional public source: Amazon Fine Food Reviews (Kaggle), which has star ratings to check `rating_guess` against.

Example row (the `input`, and the `expected` answer you label by hand):
```json
{
  "input": "The coffee tastes great and the price is fair, but the bag arrived split open and it took 9 days to come.",
  "expected": {
    "aspects": [
      {
        "aspect": "quality",
        "sentiment": "positive"
      },
      {
        "aspect": "price",
        "sentiment": "positive"
      },
      {
        "aspect": "packaging",
        "sentiment": "negative"
      },
      {
        "aspect": "delivery",
        "sentiment": "negative"
      }
    ],
    "rating_guess": 3,
    "would_recommend": true
  }
}
```

### Syed Taha Hussaini · Meeting notes action-item extractor
Paste meeting notes or a transcript; the app extracts `decisions` (list), `action_items` (task, owner, due date or null), `open_questions` and `next_meeting` (or null), then writes the follow-up email.
**Judge:** scores the email on including every action item with its owner, clarity and no invented deadlines.
**Data:** at least 20 labelled examples; synthetic (written by you or generated) is fine. Write your own: vary the length and style, and leave some owners or dates missing.

Example row (the `input`, and the `expected` answer you label by hand):
```json
{
  "input": "Agreed to launch the beta on 10 Nov. Priya to finish the login page by Friday. Someone needs to check the pricing copy. Still unsure whether we support Safari. Next catch-up Monday 10am.",
  "expected": {
    "decisions": [
      "Launch the beta on 10 Nov"
    ],
    "action_items": [
      {
        "task": "Finish the login page",
        "owner": "Priya",
        "due": "Friday"
      },
      {
        "task": "Check the pricing copy",
        "owner": null,
        "due": null
      }
    ],
    "open_questions": [
      "Do we support Safari?"
    ],
    "next_meeting": "Monday 10am"
  }
}
```

### Toni Miran Borders · Travel request planner
Type a free-text trip request ("4 days in Lisbon in May, £800, love food and museums"); the app extracts `destination`, `days`, `month`, `budget` + `currency`, `travellers`, `interests` and `constraints`, then writes a day-by-day plan.
**Judge:** scores the plan on respecting every constraint (days, budget, interests) and being realistic.
**Data:** at least 20 labelled examples; synthetic (written by you or generated) is fine. Write your own, including vague and contradictory requests.

Example row (the `input`, and the `expected` answer you label by hand):
```json
{
  "input": "4 days in Lisbon in May for me and my partner, about £800 total, we love food and museums, no early mornings please.",
  "expected": {
    "destination": "Lisbon",
    "days": 4,
    "month": "May",
    "budget": 800,
    "currency": "GBP",
    "travellers": 2,
    "interests": [
      "food",
      "museums"
    ],
    "constraints": [
      "no early mornings"
    ]
  }
}
```

---

## Presentation (Tuesday 3 November, 10 minutes)

1. Live demo: `docker compose up --build`, then the Streamlit app.
2. Your prompting techniques and the accuracy table: which won and why.
3. Your judge: rubric, agreement with your own scores, and one case where it got it wrong.
4. What you would improve next.

Push to GitHub and add the repo link as a comment on your Week 4 Trello card.
