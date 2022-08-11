from dataclasses import dataclass
from datetime import date
import json

@dataclass(frozen=True, order=True)
class Tag:
  name: str

@dataclass(frozen=True, order=True)
class Challenge:
  name: str
  tags: frozenset[Tag]

@dataclass(frozen=True, order=True)
class Attempt:
  challenge: Challenge
  date: date
  rating: int

def load_data() -> tuple[set[Tag], set[Challenge], set[Attempt]]:
  with open('data.json') as f:
    data = json.load(f)
    tags = {Tag(name=x['name']) for x in data['tags']}
    challenges = {Challenge(name=x['name'], tags=frozenset(t for t in tags if t.name in x['tags'])) for x in data['challenges']}
    attemps = {Attempt(challenge=[c for c in challenges if c.name in x['challenge']][0], date=date.fromisoformat(x['time']), rating=x['rating']) for x in data['attempts']}
    return tags, challenges, attemps

def report(tags: set[Tag], challenges: set[Challenge], attempts: set[Attempt]) -> None:
  """Get scores for challenges and tags"""
  challenge_scores = {c: 0 for c in challenges}
  for a in attempts:
    # Attempt rating is from 1 to 5, and we decrease it by 1 every week for the scoring
    # Challenge scoring is a sum of scoring of all attempts
    challenge_scores[a.challenge] += max(0, a.rating - (date.today() - a.date).days // 7)
  # Tag scoring is a sum of scoring of all challenges that have the tag
  tag_scores = {t: 0 for t in tags}
  for c in challenges:
    for t in c.tags:
      tag_scores[t] += challenge_scores[c]
  # Print the results
  # Sort the challenges and tags by score
  print('Challenge scores:')
  for c, score in sorted(challenge_scores.items(), key=lambda x: x[1], reverse=True):
    print(f'  {c.name}: {score}')
  print('Tag scores:')
  for t, score in sorted(tag_scores.items(), key=lambda x: x[1], reverse=True):
    print(f'  {t.name}: {score}')

def main() -> None:
  tags, challenges, attempts = load_data()
  report(tags=tags, challenges=challenges, attempts=attempts)

if __name__ == '__main__':
  main()