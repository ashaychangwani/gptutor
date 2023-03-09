## GPTutor
This project was created for HackNYU 2023. It aims to create a course specific bot that can act as a tutor. This bot would use the GPT model's ability to parse natural language, yet use the course content as the source of ground truth. This would allow the bot to answer questions that are specific to the course content, and provide a more personalized experience for the student. Additionally, the professor would be able to add to the bot's knowledge base by adding correct answers to questions that the bot gets wrong. Hence, the bot learns and can then answer questions better in the future. 

## Inspiration
Each professor teaches their course material in a unique manner. They might pick and choose the concepts they teach or use technical vocabulary in unconventional ways. Furthermore, the order in which they teach these concepts varies from professor to professor. All this can make searching for answers on external resources confusing for students, who may be inundated with concepts they haven't learned yet, or with concepts they have learned but which are now discussed in a different manner or context than they were in class.  And since we cannot increase the number of teachers, or the amount of extra time teachers spend in office hours, our GPTBot can fill this gap by providing students a source of inquiry that is always available to them.

## What it does
Professors upload their course material (readings, lectures, syllabus, etc.) to our server. Our system preprocesses this data, including transcribing the lectures to text. Once we construct a corpus from all the lesson materials taught up to the present moment, we use it to fine-tune a GPT-3 instance. 

Students can then interact with a bot on their class's Discord server and ask it questions in the same way they would ask their professor. In this regard, it's like having infinite clones of their professor! Except these clones are available 24/7 and have instant, accurate recall. 

Furthermore, students can improve the bot by giving correct answers a thumbs-up, which adds the Q&A interaction to the model's corpus, meaning that whenever that question is asked in the future, the bot will know the correct answer. Answers students think are incorrect can be given a thumbs-down, in which case the professor will be pinged. Once the professor gives the correct answer, this answer is added to the corpus in the same way as above. 

## How we built it

1. We first built a proof of concept by utilizing OpenAI GPT-3 (Davinci) on a small website created by a professor to check whether we can get answers to our prompt.
2. Next we built a discord bot using discord.py and Python
3. Next we took the proof of concept code and turned it into a Flask application so we can service prompts coming in from the discord bot
4. We also used the Huggingface Speech2Text/Google Cloud Speech API for lecture transcription which we added to extend our proof of concept work.

## Technical Specification
1. We first parse the entire course material into embeddings. This would allow us to find relevant content for the queries in future steps.
2. Next, we extract embeddings from the query. By using a similarity score, we can extract all relevant sections from the knowledge base.
3. Using prompt engineering, and using the strong natural language processing capabilities of GPT-3, we can generate answers to the query. Along with the query, we also pass the relevant sections from the knowledge base to the model. This allows the model to generate answers that are relevant to the query, and the course material.

## Challenges we ran into
Some challenges we ran into were:
1. Rate limits with the OpenAI API calls on the free tier
2. Massive data and limits to the query that GPT3 can handle
3. Embedding mappings for all the text
4. Setting up the discord bot and creating a thread, and having the bot reply within a thread.

## Accomplishments that we're proud of
1. The discord bot
2. The GPT model that answers questions relevant to the slides/lectures

## What we learned
1. Prompt engineering
2. Discord Bot development
3. A full stack experience of combing an AI model, a flask app and a discord client app


## What's next for Tutor Bot
1. Integration into Brightspace, Campuswire, and any other platform primarily used by NYU students to interact with their coursework, professors, and classmates. 
2. Train the GPTutor model on additional lecture videos, homework/assignments for each course for individual professors to get more context for our answers. 