"""English / Verbal Ability: original lessons, passages and questions."""

from app.seed.builders import ex, q, rule, topic

ERR = ["A", "B", "C", "No error"]

VERBAL_PASSAGES = {
    "rc-small-steps": {
        "title": "The habit of small steps",
        "body": (
            "Many students prepare for placement tests by studying for ten hours the night before. Research on memory "
            "suggests this is one of the least effective ways to learn. When we cram, information enters short-term memory "
            "but is quickly forgotten, because the brain has had no chance to consolidate it. Spacing practice over several "
            "days works far better. Each time you return to a topic after a gap, you have to work slightly harder to recall "
            "it, and that effort strengthens the memory.\n\n"
            "A second habit that helps is testing yourself instead of re-reading. Re-reading notes feels productive because "
            "the material looks familiar, but familiarity is not the same as being able to use the knowledge. Answering "
            "questions forces you to retrieve what you know, which exposes gaps early, while there is still time to fix them.\n\n"
            "Neither habit requires extra hours. A student who spends forty minutes a day answering practice questions over "
            "three weeks will usually outperform one who spends the same total time cramming. The difference lies not in "
            "effort but in how that effort is arranged."
        ),
    },
    "rc-solar-lanterns": {
        "title": "Solar lanterns in rural schools",
        "body": (
            "In several villages, schoolchildren once did their homework by the light of kerosene lamps. The lamps were "
            "cheap to buy but expensive to run, and their smoke irritated the eyes and lungs. A few years ago, a non-profit "
            "group began distributing small solar lanterns that charge during the day and give four to five hours of light "
            "at night.\n\n"
            "The results surprised even the organisers. Teachers reported that homework completion rose noticeably within a "
            "term. Families saved money that had previously gone on fuel, and some used the savings to buy books. However, "
            "the programme also ran into problems. Lanterns that broke were hard to repair locally, because spare parts had "
            "to come from the city.\n\n"
            "The organisers have since trained young people in each village to fix the lanterns. This has created small "
            "jobs and kept more lanterns working. The lesson, they say, is that a good product is only half the solution; "
            "the other half is making sure it can be looked after where it is used."
        ),
    },
    "rc-remote-work": {
        "title": "Remote work and new team members",
        "body": (
            "When offices closed suddenly, many companies discovered that their employees could work productively from "
            "home. Meetings moved online, and questions that once needed a walk down the corridor now needed a message. For "
            "people who valued quiet time, the change was welcome: they reported fewer interruptions and more time for "
            "focused work.\n\n"
            "Yet managers noticed something less visible. New employees, who had never met their colleagues in person, took "
            "longer to settle in. They were less likely to ask 'small' questions, worried that a message would seem like a "
            "bother, and so they struggled with problems that a quick chat would have solved.\n\n"
            "Several firms now use a hybrid approach. Teams meet in person on a few fixed days, which are used for "
            "discussion and mentoring, while focused work happens at home. Whether this balance is ideal is still debated, "
            "but it suggests that the real question is not 'office or home' but 'which work suits which place'."
        ),
    },
}

VERBAL_TOPICS = [
    topic(
        "grammar",
        "Grammar",
        "Parts of speech, pronouns, adjectives, adverbs and comparisons.",
        """
Grammar questions in placement tests check whether you can spot what sounds wrong to a careful reader. You don't need every rule in a grammar book, just the ones tested again and again.

Start with the parts of speech. A noun names something; a pronoun replaces a noun; a verb shows action or state; an adjective describes a noun ("a tired worker"); an adverb describes a verb, adjective or another adverb ("she sings beautifully"). Many errors come from using an adjective where an adverb belongs: "He runs quick" should be "He runs quickly".

Pronouns change form depending on their job. Use I, he, she, we, they as subjects and me, him, her, us, them as objects. Test a pair by removing the other person: "The manager asked Ravi and me" works because "asked me" works.

For comparisons, use -er or more for two things and -est or most for three or more, never both together. "More smarter" and "most tallest" are always wrong.
""",
        [
            "Adjectives describe nouns; adverbs describe verbs.",
            "Subject pronouns: I, he, she. Object pronouns: me, him, her.",
            "Never double a comparison (more smarter, most tallest).",
        ],
        [
            rule("Adverb of manner", "adjective + -ly: quick → quickly"),
            rule("Pronoun test", "remove the other noun: 'asked Ravi and me' → 'asked me'"),
            rule("Comparative / superlative", "two things: -er / more;  three or more: -est / most"),
            rule("Uncountable nouns", "news, advice, information, furniture take singular verbs"),
        ],
        [
            "Words like news, mathematics and physics look plural but are singular.",
            "'Between you and me' is correct; 'between you and I' is not.",
        ],
        [
            ex("Correct the sentence: \"She sings beautiful.\"",
               ["'Beautiful' is an adjective, but it describes how she sings, which is a verb.", "A verb needs an adverb: beautifully."],
               "She sings beautifully."),
            ex("Correct the sentence: \"This is between you and I.\"",
               ["'Between' is a preposition and takes object pronouns.", "So 'I' must become 'me'."], "This is between you and me."),
        ],
        [
            q("Choose the grammatically correct sentence.", ["He runs quick.", "He runs quickly.", "He run quickly.", "He running quick."], "B",
              "'Runs' needs an adverb (quickly), and 'he' takes 'runs'.", "easy"),
            q("What part of speech is 'quietly' in: She quietly closed the door?", ["Adjective", "Verb", "Adverb", "Noun"], "C",
              "'Quietly' tells us how she closed the door, so it describes a verb: an adverb.", "easy"),
            q("Choose the correct pronoun: The manager asked Ravi and ___ to stay late.", ["I", "me", "myself", "mine"], "B",
              "Remove 'Ravi and': 'asked me to stay late'. The object form is 'me'."),
            q("Choose the correct form: This road is ___ than the old one.", ["more wide", "widest", "most wider", "wider"], "D",
              "Two roads are compared, so use the comparative 'wider'."),
        ],
        [
            q("Which word is a conjunction in: I wanted to go, but it was raining?", ["wanted", "but", "raining", "to"], "B",
              "'But' joins two clauses, so it is a conjunction.", "easy"),
            q("Choose the grammatically correct sentence.",
              ["She is more smarter than her brother.", "She is smartest than her brother.", "She is smarter than her brother.",
               "She is most smart than her brother."], "C", "Comparing two people needs 'smarter', without 'more'."),
            q("Choose the correct reflexive pronoun: They prepared the presentation by ___.", ["theirselves", "themself", "their own", "themselves"],
              "D", "The reflexive form of 'they' is 'themselves'. 'Theirselves' is not a word."),
            q("Choose the correct word: He doesn't have ___ money left.", ["any", "some", "no", "none"], "A",
              "Negative sentences use 'any': 'doesn't have any money'. 'No' would create a double negative."),
            q("Choose the grammatically correct sentence.", ["The news are good.", "The news were good.", "The news be good.", "The news is good."],
              "D", "'News' is an uncountable noun and takes a singular verb."),
            q("Which word is an adjective in: The workers rested under a shady tree?", ["workers", "rested", "shady", "under"], "C",
              "'Shady' describes the noun 'tree', so it is an adjective."),
        ],
    ),
    topic(
        "tenses",
        "Tenses",
        "Choose the right verb form for past, present and future actions.",
        """
Tenses show when something happens. English has three times (past, present, future), and each has four forms: simple, continuous, perfect and perfect continuous. Placement questions mostly test the difference between these forms.

The simple present is for habits and facts ("The sun rises in the east"). The present continuous is for actions happening now ("Look! The baby is sleeping"). The present perfect links the past to now ("I have lived here since 2019"), and it is never used with a finished past time like "yesterday".

The past perfect shows which of two past events happened first: "By the time we reached, the train had left." The future perfect says something will be complete by a future point: "By next year, she will have completed her degree."

Time words are your best clue. Yesterday, last year and ago signal the simple past. Since and for with an ongoing situation signal a perfect tense. Now, look and at the moment signal a continuous tense.
""",
        [
            "Habits and facts: simple present.",
            "Finished past time (yesterday, ago): simple past, not present perfect.",
            "Since/for with an ongoing situation: perfect or perfect continuous.",
            "Earlier of two past actions: past perfect.",
        ],
        [
            rule("Present perfect", "has / have + past participle"),
            rule("Past perfect", "had + past participle"),
            rule("Perfect continuous", "has / had been + verb-ing"),
            rule("First conditional", "If + present, will + verb"),
        ],
        [
            "'Since' is followed by a point in time (since 2019); 'for' by a duration (for five years).",
            "Never write 'have seen … yesterday'. Use 'saw … yesterday'.",
        ],
        [
            ex("Correct the sentence: \"I have seen that film yesterday.\"",
               ["'Yesterday' is a finished past time.", "Finished past times take the simple past, not the present perfect."],
               "I saw that film yesterday."),
            ex("Complete: \"By next year, she ___ her degree.\"",
               ["'By next year' marks a point in the future.", "Something complete before a future point takes the future perfect."],
               "will have completed"),
        ],
        [
            q("She ___ to college every day.", ["go", "goes", "going", "gone"], "B", "A daily habit takes the simple present; 'she' needs 'goes'.", "easy"),
            q("They ___ football when it started to rain.", ["played", "are playing", "were playing", "have played"], "C",
              "An action in progress when another past action interrupted it takes the past continuous."),
            q("I ___ in Pune since 2019.", ["have lived", "live", "lived", "am living"], "A",
              "'Since 2019' describes a situation continuing to now, so use the present perfect."),
            q("By the time we reached the station, the train ___.", ["left", "has left", "leaves", "had left"], "D",
              "The train left before we reached, the earlier of two past actions, so use the past perfect."),
        ],
        [
            q("Look! The baby ___.", ["sleeps", "is sleeping", "slept", "has slept"], "B", "'Look!' shows the action is happening now: present continuous.", "easy"),
            q("If it rains tomorrow, we ___ the match.", ["will postpone", "postponed", "would have postponed", "had postponed"], "A",
              "A real future possibility uses: If + present, will + verb."),
            q("He ___ for three hours when the power went off.", ["has been studying", "is studying", "had been studying", "studies"], "C",
              "An action continuing up to a past moment takes the past perfect continuous.", "hard"),
            q("Choose the correct sentence.",
              ["I have finished my work yesterday.", "I had finish my work yesterday.", "I finishing my work yesterday.", "I finished my work yesterday."],
              "D", "'Yesterday' is a finished past time, so use the simple past."),
            q("Next month, she ___ here for ten years.", ["works", "will have worked", "will work", "has worked"], "B",
              "Ten years will be complete by a future point, so use the future perfect.", "hard"),
            q("The sun ___ in the east.", ["rose", "is rising", "rises", "has risen"], "C", "Universal facts take the simple present.", "easy"),
        ],
    ),
    topic(
        "subject-verb-agreement",
        "Subject-Verb Agreement",
        "Match singular and plural verbs to their real subject.",
        """
A singular subject takes a singular verb, and a plural subject takes a plural verb. That sounds simple, but placement questions hide the real subject behind extra words.

First find the true subject. In "The quality of these apples is poor", the subject is "quality", not "apples". Phrases like along with, as well as, together with and in addition to don't change the subject: "The captain, along with his players, was praised."

Some words are always singular: each, every, either, neither, everyone, anybody. "Each of the boys has a bicycle." With either…or and neither…nor, the verb agrees with the nearer subject: "Neither the teacher nor the students were present."

A few special cases come up often. "A number of" means many and takes a plural verb; "the number of" is a single number and takes a singular verb. Amounts of time, money or distance treated as one quantity are singular: "Ten kilometres is a long walk." Collective nouns like committee or team are usually singular when acting as one group.
""",
        [
            "Find the real subject; ignore phrases in between.",
            "Each, every, either, neither → singular verb.",
            "Either/or, neither/nor → agree with the nearer subject.",
        ],
        [
            rule("A number of / The number of", "plural verb / singular verb"),
            rule("Along with, as well as", "verb follows the first subject"),
            rule("Amounts as one unit", "singular: 'Five hundred rupees is enough'"),
            rule("Two nouns forming one idea", "singular: 'Bread and butter is my breakfast'"),
        ],
        [
            "Subjects that look plural but are singular: news, mathematics, physics, economics.",
            "Read the sentence without the middle phrase to hear the agreement clearly.",
        ],
        [
            ex("Correct: \"Neither the teacher nor the students was present.\"",
               ["With neither…nor, the verb agrees with the nearer subject.", "The nearer subject is 'students', which is plural."],
               "Neither the teacher nor the students were present."),
            ex("Correct: \"The captain, along with his players, were praised.\"",
               ["'Along with his players' doesn't change the subject.", "The subject is 'the captain', which is singular."],
               "The captain, along with his players, was praised."),
        ],
        [
            q("Each of the boys ___ a bicycle.", ["have", "are having", "has", "were having"], "C", "'Each' is singular, so it takes 'has'.", "easy"),
            q("A number of students ___ absent today.", ["are", "is", "was", "has been"], "A", "'A number of' means many, so the verb is plural."),
            q("Either Ravi or his friends ___ coming.", ["is", "was", "has", "are"], "D", "The verb agrees with the nearer subject, 'friends', which is plural."),
            q("Ten kilometres ___ a long distance to walk.", ["are", "is", "were", "have been"], "B",
              "A distance treated as one quantity takes a singular verb."),
        ],
        [
            q("The committee ___ reached its decision.", ["have", "are", "has", "were"], "C",
              "The committee acts as one body ('its decision'), so the verb is singular."),
            q("Bread and butter ___ my favourite breakfast.", ["is", "are", "were", "have been"], "A",
              "'Bread and butter' is a single dish, so it takes a singular verb.", "hard"),
            q("The teacher, as well as her students, ___ excited.", ["were", "are", "have been", "is"], "D",
              "'As well as her students' doesn't change the subject, 'the teacher', which is singular."),
            q("Neither of the answers ___ correct.", ["are", "is", "were", "have been"], "B", "'Neither' is singular, so it takes 'is'."),
            q("The number of applicants ___ increased this year.", ["have", "are", "were", "has"], "D",
              "'The number of' refers to a single number, so it takes a singular verb."),
            q("Mathematics ___ my favourite subject.", ["are", "were", "is", "have"], "C", "'Mathematics' looks plural but is singular.", "easy"),
        ],
    ),
    topic(
        "articles-prepositions",
        "Articles and Prepositions",
        "Use a, an and the correctly, and pick the right preposition.",
        """
Articles are short words that cause many errors. Use "a" before a consonant sound and "an" before a vowel sound. Sound matters, not spelling: "an hour" (silent h), "an honest man", but "a university" and "a one-rupee coin" (they start with a 'y' or 'w' sound).

Use "the" when the reader knows exactly which thing you mean, for unique things (the sun, the internet), for rivers, oceans and mountain ranges (the Ganga, the Himalayas), and before superlatives (the tallest building).

Prepositions show relationships of time and place. For time: at with clock times (at 10 a.m.), on with days and dates (on Monday), in with months, years and parts of the day (in April, in the morning). "Since" marks a starting point, while "for" marks a duration.

Other common pairs: between two people but among three or more; in (inside, at rest) versus into (movement inside); and fixed phrases such as "senior to", "prefer to" and "apologise for".
""",
        [
            "a/an depends on the sound, not the letter.",
            "Use 'the' for specific or unique things.",
            "at + time, on + day/date, in + month/year.",
            "since + starting point, for + duration.",
        ],
        [
            rule("a vs an", "an hour, an honest man; a university, a European"),
            rule("Time prepositions", "at 5 p.m. · on Monday · in July · in 2024"),
            rule("between / among", "between two · among three or more"),
            rule("in / into", "in = position · into = movement inside"),
        ],
        [
            "No article before most proper nouns (India, Ravi), but use 'the' for rivers and oceans.",
            "Fixed phrases: 'interested in', 'good at', 'afraid of', 'depend on'.",
        ],
        [
            ex("Correct: \"He is a honest man.\"", ["'Honest' starts with a silent h, so it begins with a vowel sound.", "Use 'an' before a vowel sound."],
               "He is an honest man."),
            ex("Correct: \"I have lived here since five years.\"",
               ["'Five years' is a length of time, not a starting point.", "Durations take 'for'."], "I have lived here for five years."),
        ],
        [
            q("She is ___ engineer.", ["a", "the", "an", "no article"], "C", "'Engineer' starts with a vowel sound, so use 'an'.", "easy"),
            q("We will meet ___ Monday.", ["in", "at", "by", "on"], "D", "Days take 'on'.", "easy"),
            q("He is ___ university professor.", ["a", "an", "the", "no article"], "A",
              "'University' starts with a 'yoo' sound, a consonant sound, so use 'a'."),
            q("The book is ___ the table.", ["in", "on", "into", "at"], "B", "Something resting on a surface takes 'on'.", "easy"),
        ],
        [
            q("___ Ganga is a holy river.", ["A", "An", "The", "No article"], "C", "Rivers take 'the'."),
            q("The meeting starts ___ 10 a.m.", ["at", "on", "in", "by"], "A", "Clock times take 'at'.", "easy"),
            q("Divide the sweets ___ the three children.", ["between", "among", "with", "within"], "B", "Use 'among' for three or more."),
            q("He has been ill ___ last Monday.", ["for", "from", "by", "since"], "D", "'Last Monday' is a starting point, so use 'since'."),
            q("She jumped ___ the swimming pool.", ["in", "on", "into", "at"], "C", "Movement from outside to inside takes 'into'."),
            q("It was ___ unique experience.", ["an", "a", "the", "no article"], "B",
              "'Unique' starts with a 'yoo' sound, so use 'a'.", "hard"),
        ],
    ),
    topic(
        "vocabulary",
        "Vocabulary",
        "Word meanings, one-word substitutions and common idioms.",
        """
Vocabulary questions come in three forms: the meaning of a word, a single word that replaces a phrase (one-word substitution), and the meaning of an idiom.

Build vocabulary through roots, not lists. Many English words come from Latin and Greek parts: "omni" means all (omniscient: knowing everything), "poly" means many (polyglot: speaking many languages), "phobia" means fear (acrophobia: fear of heights), and "in-/im-" often means not (incorrigible: cannot be corrected). Learning a root unlocks dozens of words.

Idioms don't mean what their words say. "Break the ice" has nothing to do with ice; it means starting a conversation in an awkward situation. Learn idioms with an example sentence, because the context is what makes them stick.

In the test, if you don't know a word, eliminate options whose meaning you're sure doesn't fit, and look for root clues in what's left.
""",
        [
            "Learn word roots: omni (all), poly (many), phobia (fear), bene (good), mal (bad).",
            "Idioms have figurative meanings; learn them in sentences.",
            "Eliminate the options you can rule out first.",
        ],
        [
            rule("omni-", "all: omniscient, omnipresent"),
            rule("poly-", "many: polyglot, polygon"),
            rule("-phobia", "fear of: acrophobia (heights), claustrophobia (closed spaces)"),
            rule("bene- / mal-", "good / bad: benevolent, malicious"),
        ],
        [
            "Read a short English newspaper article daily and note three new words with their sentences.",
            "One-word substitutions often end in -cide (killing), -cracy (rule) or -logy (study of).",
        ],
        [
            ex("Give one word for: one who knows everything.", ["'Omni' means all; 'scient' relates to knowing."], "Omniscient"),
            ex("What does the idiom 'bite the bullet' mean?", ["It comes from soldiers biting on something to endure pain.", "Today it means facing something unpleasant bravely."],
               "To face a difficult situation with courage."),
        ],
        [
            q("One word for 'a person who cannot be corrected':", ["invincible", "indelible", "incorrigible", "infallible"], "C",
              "Incorrigible = impossible to correct or reform. Invincible = unbeatable; indelible = can't be erased; infallible = never wrong."),
            q("What does 'meticulous' mean?", ["Careless", "Very careful about details", "Fearless", "Talkative"], "B",
              "Meticulous means showing great attention to detail.", "easy"),
            q("What does the idiom 'break the ice' mean?",
              ["To start a conversation in an awkward situation", "To cause an argument", "To leave suddenly", "To make a mistake"], "A",
              "Breaking the ice means easing initial awkwardness, often by starting a conversation."),
            q("One word for 'a person who speaks many languages':", ["linguist", "bilingual", "orator", "polyglot"], "D",
              "Poly (many) + glot (tongue). A bilingual speaks two; a linguist studies languages."),
        ],
        [
            q("One word for 'a place where birds are kept':", ["aviary", "apiary", "aquarium", "kennel"], "A",
              "An aviary houses birds. An apiary houses bees, an aquarium fish, and a kennel dogs."),
            q("What does 'ambiguous' mean?", ["Very clear", "Open to more than one interpretation", "Extremely large", "Full of ambition"], "B",
              "Something ambiguous can be understood in more than one way."),
            q("What does 'a blessing in disguise' mean?",
              ["A hidden gift", "A religious ceremony", "Something good that seemed bad at first", "A secret plan"], "C",
              "It describes an apparent misfortune that turns out to be beneficial."),
            q("One word for 'fear of heights':", ["claustrophobia", "hydrophobia", "agoraphobia", "acrophobia"], "D",
              "Acro means height. Claustrophobia = closed spaces, hydrophobia = water, agoraphobia = open or crowded places.", "hard"),
            q("What does 'frugal' mean?", ["Wasteful", "Economical; avoiding waste", "Fruitful", "Generous"], "B",
              "A frugal person spends carefully and avoids waste."),
            q("What does the idiom 'hit the nail on the head' mean?",
              ["To describe exactly what is causing a problem", "To work with tools", "To hurt someone", "To make a loud noise"], "A",
              "It means to say something exactly right or identify the precise point."),
        ],
    ),
    topic(
        "synonyms-antonyms",
        "Synonyms and Antonyms",
        "Find words with the same or opposite meaning.",
        """
A synonym has the same (or nearly the same) meaning as a word; an antonym has the opposite meaning. These questions are quick if you know the word and slow if you don't, so the goal is to build a strong working vocabulary.

Read the question carefully. Synonym and antonym questions are often mixed in one section, and choosing a synonym when the question asked for an antonym is the most common mistake. The test-setters usually include the synonym among the antonym options for exactly that reason.

When you know the word only vaguely, decide first whether it's positive or negative ("benevolent" sounds kind, "malicious" sounds harmful). That alone often removes two options.

Learn words in pairs: abundant/scarce, expand/contract, transparent/opaque, humble/arrogant. One memory gives you both a synonym and an antonym.
""",
        [
            "Check whether the question asks for a synonym or an antonym.",
            "Decide if the word is positive or negative to eliminate options.",
            "Learn words in opposite pairs.",
        ],
        [
            rule("Synonym", "same meaning: candid ≈ frank"),
            rule("Antonym", "opposite meaning: scarce ↔ plentiful"),
            rule("Common opposite prefixes", "un-, in-, im-, dis-, non-"),
        ],
        [
            "The synonym is often planted among antonym options as a trap.",
            "If two options mean the same thing, neither is likely to be the unique answer.",
        ],
        [
            ex("Find a synonym of 'abundant'.", ["Abundant means existing in large quantities.", "A word with the same meaning is 'plentiful'."], "Plentiful"),
            ex("Find an antonym of 'ancient'.", ["Ancient means very old.", "Its opposite is 'modern'."], "Modern"),
        ],
        [
            q("Choose the synonym of 'abundant'.", ["scarce", "plentiful", "empty", "rare"], "B", "Abundant means plentiful. Scarce and rare are its antonyms.", "easy"),
            q("Choose the antonym of 'ancient'.", ["old", "historic", "modern", "antique"], "C", "Ancient means very old; modern is its opposite.", "easy"),
            q("Choose the synonym of 'candid'.", ["frank", "secretive", "polite", "shy"], "A", "Candid means open and honest: frank."),
            q("Choose the antonym of 'expand'.", ["grow", "increase", "stretch", "contract"], "D", "Expand means get bigger; contract means get smaller."),
        ],
        [
            q("Choose the synonym of 'diligent'.", ["lazy", "careless", "hardworking", "clever"], "C", "Diligent means hardworking and careful."),
            q("Choose the antonym of 'scarce'.", ["plentiful", "rare", "few", "limited"], "A", "Scarce means in short supply; plentiful is its opposite."),
            q("Choose the synonym of 'obsolete'.", ["modern", "outdated", "useful", "popular"], "B", "Obsolete means no longer in use: outdated."),
            q("Choose the antonym of 'humble'.", ["modest", "polite", "simple", "arrogant"], "D", "Humble means modest; arrogant is its opposite.", "easy"),
            q("Choose the synonym of 'benevolent'.", ["cruel", "kind", "jealous", "angry"], "B", "Benevolent means well-meaning and kind ('bene' = good)."),
            q("Choose the antonym of 'transparent'.", ["clear", "visible", "opaque", "obvious"], "C",
              "Transparent means see-through; opaque means not letting light through.", "hard"),
        ],
    ),
    topic(
        "sentence-correction",
        "Sentence Correction",
        "Choose the grammatically correct version of a sentence.",
        """
Sentence correction questions give you a sentence (or part of one) and ask for the best version. The error is almost always one of a small set: verb form, subject–verb agreement, tense, a wrong preposition in a fixed phrase, a wrong comparison, or a redundant word.

Work in a fixed order. First check the verb: does it agree with its subject, and is the tense right? Then check pronouns and comparisons. Finally check fixed phrases: "senior to" (not "than"), "prefer A to B", "look forward to + -ing", "one of the + plural noun".

Be careful with "No improvement". It is the right answer sometimes, but only when you've checked every part and found nothing wrong. Don't choose it just because nothing jumps out.

Also watch for double negatives hidden in words like "unless" (which already means "if not") and "hardly" or "scarcely" (which already sound negative).
""",
        [
            "Check verbs first: agreement and tense.",
            "Then check pronouns, comparisons and fixed phrases.",
            "Choose 'No improvement' only after checking everything.",
        ],
        [
            rule("Comparatives with 'to'", "senior to, junior to, superior to, prefer … to"),
            rule("look forward to", "followed by verb-ing: 'look forward to meeting'"),
            rule("one of the …", "plural noun, singular verb: 'one of my friends lives'"),
            rule("Unless", "already negative: 'unless you work' not 'unless you do not work'"),
        ],
        [
            "'Hardly … when' and 'No sooner … than' are fixed pairs.",
            "Watch for verbs after 'did': 'did not know', never 'did not knew'.",
        ],
        [
            ex("Correct: \"He did not knew the answer.\"", ["After 'did', the verb stays in its base form."], "He did not know the answer."),
            ex("Correct: \"One of my friend live in Delhi.\"",
               ["'One of' is followed by a plural noun: friends.", "The subject is 'one', which is singular, so the verb is 'lives'."],
               "One of my friends lives in Delhi."),
        ],
        [
            q("Choose the correct sentence.", ["She don't like coffee.", "She doesn't likes coffee.", "She not like coffee.", "She doesn't like coffee."], "D",
              "'She' takes 'doesn't', which is followed by the base verb 'like'.", "easy"),
            q("Improve the sentence: He is senior than me.", ["senior to me", "more senior than me", "seniorer than me", "No improvement"], "A",
              "'Senior' takes 'to', not 'than'."),
            q("Improve the sentence: I am looking forward to meet you.", ["looking forward for meeting you", "looking forward to meeting you",
              "looking forward meeting you", "No improvement"], "B", "'Look forward to' is followed by the -ing form: 'meeting'."),
            q("Improve the sentence: The scenery here are beautiful.", ["The sceneries here are beautiful.", "The scenery here were beautiful.",
              "The scenery here is beautiful.", "No improvement"], "C", "'Scenery' is uncountable and takes a singular verb."),
        ],
        [
            q("Improve the sentence: He prefers tea than coffee.", ["prefers tea over than coffee", "No improvement", "prefers tea from coffee",
              "prefers tea to coffee"], "D", "'Prefer' is followed by 'to' when comparing two things."),
            q("Improve the sentence: Hardly had I reached the station when the train left.",
              ["Hardly I had reached", "Hardly had I reached … than", "No improvement", "Hardly did I reached"], "C",
              "'Hardly … when' is the correct pair, and the inverted 'had I reached' is correct. The sentence needs no change.", "hard"),
            q("Improve the sentence: Each of the players have a kit.", ["Each of the players has a kit.", "Each of the player have a kit.",
              "Each of the players are having a kit.", "No improvement"], "A", "'Each' is singular, so the verb is 'has'."),
            q("Choose the correct sentence.", ["I am working here since 2020.", "I have been working here since 2020.",
              "I worked here since 2020.", "I work here since 2020."], "B", "An action continuing from 2020 until now takes the present perfect continuous."),
            q("Improve the sentence: She is one of the best singer in the city.", ["one of the better singer", "one of the best singers",
              "one of best singer", "No improvement"], "B", "'One of the' is followed by a plural noun: singers."),
            q("Improve the sentence: Unless you do not work hard, you will fail.", ["If you do not work hard unless", "Unless you will work hard",
              "No improvement", "Unless you work hard"], "D", "'Unless' already means 'if not', so 'do not' creates a double negative.", "hard"),
        ],
    ),
    topic(
        "error-spotting",
        "Error Spotting",
        "Find which part of a sentence contains a grammatical error.",
        """
In error spotting, a sentence is split into parts labelled (A), (B), (C), and you choose the part containing the error, or "No error". It tests the same grammar as sentence correction, but you only need to locate the mistake, not fix it.

Read the whole sentence first to understand its meaning. Then check each part against the usual suspects: subject–verb agreement, tense consistency, pronoun case, articles, prepositions, and comparisons.

The error is often in the part with the verb, so check that first, but don't stop there. Many test-setters place an obviously correct-looking verb in one part and hide the real error in an article or pronoun elsewhere.

If after checking all parts you find nothing wrong, "No error" is a real possibility. Typically about one question in five has no error.
""",
        [
            "Read the whole sentence before judging any part.",
            "Check verb agreement and tense first, then pronouns, articles and prepositions.",
            "'No error' is a legitimate answer.",
        ],
        [
            rule("If I were", "unreal conditions use 'were' for all subjects"),
            rule("Superlatives", "never 'most tallest'; use 'the tallest'"),
            rule("Reflexive pronouns", "'myself' only when the subject is also 'I'"),
            rule("Collective uncountables", "furniture, luggage, equipment take singular verbs"),
        ],
        [
            "Mark the subject and its verb in each sentence. Most errors live between them.",
            "'Advice', 'information' and 'furniture' never take 'an' and are never plural.",
        ],
        [
            ex("Find the error: (A) The quality of these apples / (B) are not / (C) very good.",
               ["The subject is 'the quality', not 'apples'.", "'Quality' is singular, so 'are' should be 'is'."], "Part B"),
            ex("Find the error: (A) She has been working / (B) in this company / (C) since five years.",
               ["'Five years' is a duration.", "Durations take 'for', not 'since'."], "Part C"),
        ],
        [
            q("Find the part with an error: (A) Neither of the two candidates / (B) were selected / (C) for the job.", ERR, "B",
              "'Neither' is singular, so 'were' should be 'was'."),
            q("Find the part with an error: (A) He gave me / (B) an useful advice / (C) about the interview.", ERR, "B",
              "'Useful' begins with a 'yoo' sound (so 'a', not 'an'), and 'advice' is uncountable. Write 'some useful advice'."),
            q("Find the part with an error: (A) The children / (B) are playing / (C) in the park.", ERR, "D",
              "Every part is correct: plural subject, plural verb, correct preposition.", "easy"),
            q("Find the part with an error: (A) She did not / (B) went to / (C) the market yesterday.", ERR, "B",
              "After 'did not', use the base form 'go', not 'went'.", "easy"),
        ],
        [
            q("Find the part with an error: (A) Each of the girls / (B) have submitted / (C) her assignment.", ERR, "B",
              "'Each' is singular, so 'have' should be 'has'."),
            q("Find the part with an error: (A) All the furniture / (B) have been / (C) moved upstairs.", ERR, "B",
              "'Furniture' is uncountable and takes a singular verb: 'has been'."),
            q("Find the part with an error: (A) If I was you, / (B) I would apply / (C) for that job.", ERR, "A",
              "Unreal conditions use 'were': 'If I were you'.", "hard"),
            q("Find the part with an error: (A) He is the most tallest / (B) boy / (C) in our class.", ERR, "A",
              "'Most tallest' is a double superlative. It should be 'the tallest'.", "easy"),
            q("Find the part with an error: (A) The train / (B) had left / (C) before we reached the station.", ERR, "D",
              "The past perfect correctly marks the earlier of two past events. There is no error."),
            q("Find the part with an error: (A) My brother and myself / (B) went to / (C) the interview together.", ERR, "A",
              "'Myself' can't be a subject. It should be 'My brother and I'."),
        ],
    ),
    topic(
        "fill-in-the-blanks",
        "Fill in the Blanks",
        "Choose the word that fits the meaning and grammar of a sentence.",
        """
Fill-in-the-blank questions test vocabulary and grammar together. The right word must fit two things: the meaning of the sentence and the grammar around the blank.

Look for clue words. "So … that" shows cause and effect ("so efficient that she finished in a day"). "But", "although" and "however" signal contrast, so the blank will oppose the other half. A semicolon or "because" often means the second half explains the first.

Next, check grammar. Does the blank need a noun, verb, adjective or adverb? If the blank follows "to", it usually needs a verb; if it follows "a" or "the", a noun or adjective. This often removes two options instantly.

Phrasal verbs (give up, take effect, look after) and fixed prepositions (apologise for, capable of) are favourites, so learn them as units.
""",
        [
            "Find clue words that show cause, contrast or explanation.",
            "Check the part of speech the blank needs.",
            "Learn phrasal verbs and fixed prepositions as units.",
        ],
        [
            rule("Contrast markers", "but, although, however, yet, despite"),
            rule("Cause markers", "so … that, because, therefore, as a result"),
            rule("Common phrasal verbs", "give up (quit), take effect (start), look after (care for)"),
            rule("Fixed prepositions", "apologise for, capable of, interested in, depend on"),
        ],
        [
            "Read the sentence with your chosen word; it should sound natural aloud.",
            "If two options fit the meaning, grammar usually decides.",
        ],
        [
            ex("The manager was ___ with his team's performance; he praised everyone.",
               ["The second half says he praised everyone, which is positive.", "So the blank needs a positive word."], "delighted"),
            ex("Despite his ___ efforts, he could not finish on time.",
               ["'Despite' signals contrast: he tried hard but still didn't finish.", "So the blank describes strong effort."], "strenuous"),
        ],
        [
            q("She was so ___ that she finished the whole project in a day.", ["lazy", "careless", "efficient", "slow"], "C",
              "'So … that she finished in a day' needs a positive quality: efficient.", "easy"),
            q("The new policy will ___ effect from April.", ["make", "take", "give", "bring"], "B", "The fixed phrase is 'take effect', meaning start to apply."),
            q("He apologised ___ being late.", ["for", "to", "on", "about"], "A", "The fixed preposition is 'apologise for'.", "easy"),
            q("The lecture was so ___ that several students fell asleep.", ["exciting", "lively", "interesting", "monotonous"], "D",
              "Students falling asleep shows the lecture was dull and repetitive: monotonous."),
        ],
        [
            q("To serve its southern customers better, the company has ___ a new branch in Hyderabad.", ["shut", "opened", "sold", "lost"], "B",
              "Serving customers better implies adding a branch: opened.", "easy"),
            q("He is ___ of handling pressure; he never panics.", ["capable", "able", "incapable", "capability"], "A",
              "'Capable of' is the correct phrase, and 'never panics' shows a positive meaning. 'Able' takes 'to'."),
            q("The two sisters are very different: one is outgoing and the other is ___.", ["friendly", "talkative", "reserved", "cheerful"], "C",
              "'Very different' signals contrast with 'outgoing', so: reserved."),
            q("Please ___ the form before the deadline.", ["submission", "submitting", "submitted", "submit"], "D",
              "'Please' is followed by a base verb: submit."),
            q("Her argument was so ___ that nobody could disagree.", ["weak", "unclear", "confused", "convincing"], "D",
              "Nobody disagreeing shows the argument was convincing."),
            q("The doctor advised him to ___ smoking.", ["give in", "give up", "give out", "give away"], "B",
              "'Give up' means to stop doing something.", "hard"),
        ],
    ),
    topic(
        "reading-comprehension",
        "Reading Comprehension",
        "Read a passage and answer questions on its ideas and details.",
        """
Reading comprehension (RC) gives you a passage of a few paragraphs and several questions about it. The questions usually fall into four types: main idea, specific detail, inference (what the passage suggests but doesn't state), and vocabulary in context.

Read the questions quickly first, so you know what to look for. Then read the passage once, actively: after each paragraph, say to yourself in a few words what it was about. This gives you a map for finding details later.

For detail questions, go back to the passage and find the exact line. Don't answer from memory. For inference questions, choose the option the passage supports most strongly, not something merely possible. For main-idea questions, the right answer covers the whole passage, not just one paragraph.

For vocabulary questions, the meaning in the passage matters more than the dictionary meaning. Replace the word with each option and see which keeps the sentence's meaning.
""",
        [
            "Skim the questions before reading.",
            "Summarise each paragraph in a few words as you read.",
            "Answer detail questions from the text, not memory.",
            "The main idea covers the whole passage.",
        ],
        [
            rule("Main idea", "the point the whole passage supports"),
            rule("Detail", "stated directly; find the line"),
            rule("Inference", "strongly supported but not stated word for word"),
            rule("Vocabulary in context", "substitute each option into the sentence"),
        ],
        [
            "Extreme options (always, never, all) are usually wrong in RC.",
            "An option can be true in real life and still wrong if the passage doesn't support it.",
        ],
        [
            ex("A passage explains that a bakery started delivering bread by bicycle, cutting fuel costs and arriving faster in narrow lanes. What is its main idea?",
               ["Paragraph points: the bakery changed delivery method, saved money, and delivered faster.", "The idea covering all of it: the switch to bicycles helped the business."],
               "Switching to bicycle delivery benefited the bakery."),
            ex("In the sentence 'The committee will scrutinise every application', what does 'scrutinise' mean?",
               ["The committee is checking applications.", "Substituting 'examine carefully' keeps the meaning."], "Examine carefully"),
        ],
        [
            q("According to the passage, what is the main point the author makes?",
              ["Students should study for longer hours.", "Spacing out practice and testing yourself make study time more effective.",
               "Short-term memory is more reliable than long-term memory.", "Re-reading notes is the best way to prepare."],
              "B", "The passage argues that spacing and self-testing work better than cramming, without needing extra hours.", passage="rc-small-steps"),
            q("Why, according to the passage, does re-reading notes feel productive?",
              ["Because it takes a long time", "Because teachers recommend it", "Because the material looks familiar", "Because it exposes gaps early"],
              "C", "The second paragraph says re-reading 'feels productive because the material looks familiar'.", "easy", passage="rc-small-steps"),
            q("As used in the passage, 'consolidate' most nearly means:",
              ["strengthen and settle", "forget quickly", "divide into parts", "write down"],
              "A", "The brain needs time to consolidate information, which means to make it firm and lasting.", passage="rc-small-steps"),
            q("Which student would the author expect to perform best?",
              ["One who studies ten hours the night before", "One who re-reads notes several times",
               "One who studies only on the weekend before the test", "One who answers practice questions for forty minutes daily for three weeks"],
              "D", "The final paragraph says this student will usually outperform someone who crams the same total time.", "hard", passage="rc-small-steps"),
        ],
        [
            q("What problem did the solar lantern programme face?",
              ["Children did not like the lanterns.", "Broken lanterns were hard to repair locally.",
               "The lanterns gave too little light.", "Families could not afford the lanterns."],
              "B", "The second paragraph says broken lanterns were hard to repair because spare parts came from the city.", passage="rc-solar-lanterns"),
            q("According to the passage, what did some families do with the money they saved?",
              ["Bought more kerosene", "Bought books", "Repaired their homes", "Started businesses"],
              "B", "The passage says some families used the savings to buy books.", "easy", passage="rc-solar-lanterns"),
            q("What lesson do the organisers draw from their experience?",
              ["Solar power is cheaper than kerosene.", "Children study better at night.",
               "A product succeeds only if it can be maintained where it is used.", "Non-profits should work only in cities."],
              "C", "The final sentence says a good product is half the solution; the other half is local upkeep.", passage="rc-solar-lanterns"),
            q("Why, according to the passage, did new employees take longer to settle in?",
              ["They hesitated to ask small questions over messages.", "They preferred working in the office.",
               "Their managers gave them too much work.", "They had slow internet connections."],
              "A", "The second paragraph says new employees avoided small questions, worried a message would be a bother.", passage="rc-remote-work"),
            q("In the hybrid approach described, what are the in-person days mainly used for?",
              ["Focused individual work", "Training on software", "Discussion and mentoring", "Annual reviews"],
              "C", "The third paragraph says office days are used for discussion and mentoring.", "easy", passage="rc-remote-work"),
            q("Which statement best expresses the author's conclusion?",
              ["Offices are no longer necessary.", "Everyone should work from home.",
               "Hybrid work has been proven ideal.", "The key is matching kinds of work to the right place."],
              "D", "The last sentence reframes the question as 'which work suits which place'. The passage says the hybrid balance is still debated, so C goes too far.",
              "hard", passage="rc-remote-work"),
        ],
    ),
    topic(
        "para-jumbles",
        "Para Jumbles",
        "Rearrange shuffled sentences into a logical paragraph.",
        """
A para jumble gives you four or five sentences in the wrong order, labelled P, Q, R, S, and asks for the order that forms a coherent paragraph.

Start by finding the opening sentence. It introduces the subject and can stand alone. It won't begin with a pronoun like "he" or "this", or a connector like "however" or "then", because those depend on something before them.

Next, look for mandatory pairs: two sentences that must sit together. A pronoun ("He started a shop") must come after the sentence naming that person. "Then", "next" and "finally" show sequence. "However" and "but" show a turn in the story. "As a result" follows a cause.

Finally, check time order. Dates, "first", "within ten years", "today" all fix positions. Once you have the opener and one or two pairs, usually only one option fits. Check it against the options rather than building the full order from scratch.
""",
        [
            "The opener introduces the topic and has no unexplained pronoun or connector.",
            "Find pairs: a noun before its pronoun, a cause before its result.",
            "Use time markers to fix the sequence.",
            "Eliminate options using the opener before ordering the rest.",
        ],
        [
            rule("Sequence markers", "first → then / next → finally"),
            rule("Contrast markers", "however, but, instead: come after the idea they contrast"),
            rule("Result markers", "so, therefore, as a result: come after the cause"),
        ],
        [
            "'Today' or 'now' sentences usually come near the end of a story-type jumble.",
            "If two options share the same opener, compare where they differ.",
        ],
        [
            ex("P: He started with a small shop. Q: Today, his company employs 5,000 people. R: Ramesh moved to the city in 1990. S: Within ten years, the shop became a chain.",
               ["R names Ramesh and sets the time, so it opens.", "P ('He started …') follows R.", "S grows the shop; Q ('Today') ends the story."], "RPSQ"),
            ex("P: This is why the sky looks blue. Q: Sunlight contains all colours. R: Blue light is scattered the most by air. S: When it enters the atmosphere, it is scattered.",
               ["Q introduces sunlight and opens.", "S ('it') refers to sunlight, so S follows Q.", "R explains which colour scatters most; P gives the result."],
               "QSRP"),
        ],
        [
            q("Arrange: P: Then she added sugar and stirred it well. Q: Meena boiled water in a pan. R: Finally, she poured the tea into cups. S: Next, she added tea leaves and milk.",
              ["QPSR", "QSPR", "SQPR", "QSRP"], "B", "Q opens. 'Next' (S) comes before 'Then' (P), and 'Finally' (R) ends: QSPR.", "easy"),
            q("Arrange: P: This makes them ideal for remote areas. Q: Solar panels convert sunlight into electricity. R: They need little maintenance and no fuel. S: As a result, many villages are now adopting them.",
              ["QPRS", "RQPS", "QRPS", "QRSP"], "C",
              "Q introduces solar panels. R ('They') describes them. P ('This') draws the conclusion. S ('As a result') follows: QRPS."),
            q("Arrange: P: However, he did not give up. Q: Arjun failed his first interview. R: He practised mock interviews every day. S: Three months later, he received an offer from a top company.",
              ["QPRS", "QRPS", "PQRS", "QPSR"], "A", "Q opens with Arjun. 'However' (P) turns the story, R shows effort, and S is the result: QPRS."),
            q("Arrange: P: It was invented to send messages between computers. Q: Today, billions of people use email every day. R: Email is older than the World Wide Web. S: Over time, it became a standard business tool.",
              ["RSPQ", "PRSQ", "RPQS", "RPSQ"], "D",
              "R introduces email. P ('It was invented') follows. S ('Over time') develops it, and Q ('Today') ends: RPSQ."),
        ],
        [
            q("Arrange: P: The committee reviewed all the applications. Q: The college announced a scholarship for top students. R: Ten students were finally selected. S: Hundreds of students applied within a week.",
              ["QSPR", "QPSR", "SQPR", "QSRP"], "A", "The announcement (Q), the applications (S), the review (P), the selection (R): QSPR."),
            q("Arrange: P: She noted down every new word she found. Q: Priya wanted to improve her vocabulary. R: Within a year, her reading speed had doubled. S: So she began reading an English newspaper daily.",
              ["QPSR", "SQPR", "QSRP", "QSPR"], "D", "Goal (Q), action (S, 'So'), habit (P, 'She noted'), result (R): QSPR."),
            q("Arrange: P: Because of this, they shed their leaves in winter. Q: Deciduous trees lose a lot of water through their leaves. R: Water is scarce when the ground freezes. S: Shedding leaves helps them survive the cold, dry months.",
              ["QPRS", "QRPS", "RQPS", "QRSP"], "B",
              "Q introduces the trees. R explains water scarcity. P ('Because of this') gives the response. S explains the benefit: QRPS.", "hard"),
            q("Arrange: P: The first step is to read the question carefully. Q: Many students lose marks in aptitude tests through avoidable errors. R: The second is to check units before choosing an answer. S: A simple routine can prevent most of them.",
              ["QPSR", "SQPR", "QSPR", "QSRP"], "C", "Q states the problem. S ('them') offers a routine. P and R give the first and second steps: QSPR."),
            q("Arrange: P: He then checked the logs for errors. Q: The website crashed late at night. R: The engineer on duty was alerted at once. S: Within an hour, the bug was fixed.",
              ["QRPS", "QPRS", "RQPS", "QRSP"], "A", "The crash (Q), the alert (R), the investigation (P, 'then'), the fix (S): QRPS."),
            q("Arrange: P: Instead, she started a small library in her village. Q: After retiring, Mrs. Rao could have rested at home. R: Today, over two hundred children borrow books from it. S: She began with just fifty donated books.",
              ["QSPR", "QPRS", "PQSR", "QPSR"], "D",
              "Q opens. 'Instead' (P) contrasts with resting. S describes the start, and R ('Today') ends: QPSR.", "hard"),
        ],
    ),
    topic(
        "sentence-completion",
        "Sentence Completion",
        "Choose the ending or word pair that completes a sentence logically.",
        """
Sentence completion asks you to finish a sentence so that it makes logical and grammatical sense. Sometimes you choose a whole clause; sometimes one or two words.

The first half of the sentence sets up an expectation. Connectors tell you what kind: "because" and "so" expect a cause or result; "although", "despite" and "though" expect a contrast; "unless" expects a condition; "not only … but also" expects an addition in the same direction.

For two-blank questions, solve the easier blank first and eliminate options, then check the second blank in the options that remain. Both words must fit; one good word isn't enough.

Finally, read your full sentence. It should be logical in the real world. "Because the roads were flooded, everyone went swimming in the river" is grammatical but not a sensible consequence.
""",
        [
            "Identify the connector and the expectation it creates.",
            "Contrast words need an opposite idea; cause words need a result.",
            "For two blanks, solve the easier one first.",
        ],
        [
            rule("Contrast", "although, though, despite → opposite idea"),
            rule("Cause / result", "because, so, therefore → logical consequence"),
            rule("Condition", "unless (= if not) → what happens otherwise"),
            rule("Addition", "not only … but also → same direction"),
        ],
        [
            "'The more …, the more …' sentences need a matching comparative in both halves.",
            "Reject endings that are grammatical but illogical.",
        ],
        [
            ex("Although the exam was difficult, ___",
               ["'Although' expects a contrast with 'difficult'.", "A positive outcome fits: students still managed."],
               "most students managed to finish on time."),
            ex("The speaker was so ___ that the audience remained ___ throughout.",
               ["'So … that' links cause and effect.", "An engaging speaker keeps an audience attentive."], "engaging … attentive"),
        ],
        [
            q("Because the roads were flooded, ___", ["the sun was shining.", "the schools remained closed.",
              "the traffic moved faster than usual.", "everyone went swimming in the river."], "B",
              "'Because' needs a sensible result of flooding: schools closing.", "easy"),
            q("She practised every day, so ___", ["she forgot everything.", "she stopped practising.",
              "her performance improved steadily.", "the exam was cancelled."], "C", "'So' introduces a result; daily practice leads to improvement.", "easy"),
            q("The scientist's theory was ___ by later experiments, which proved it correct.", ["confirmed", "rejected", "ignored", "questioned"], "A",
              "'Proved it correct' means the experiments confirmed the theory."),
            q("Though he is wealthy, he lives a ___ life.", ["lavish", "luxurious", "extravagant", "simple"], "D",
              "'Though' signals contrast with 'wealthy', so: simple."),
        ],
        [
            q("Unless you leave now, ___", ["you will miss the bus.", "you will catch the bus.", "the bus will wait for you.", "you left early."], "A",
              "'Unless' means 'if you don't'. If you don't leave now, you'll miss the bus."),
            q("The more you practise, ___", ["the less you know.", "the more confident you become.", "you will be tired.", "practice is boring."], "B",
              "'The more …' pairs with another 'the more …' in a matching cause–effect."),
            q("The new manager was both ___ and ___: she listened carefully and decided quickly.",
              ["rude … slow", "careless … hasty", "patient … decisive", "shy … confused"], "C",
              "Listening carefully shows patience; deciding quickly shows decisiveness.", "hard"),
            q("Not only did he finish the project early, ___", ["he was late.", "and he failed.", "the project failed.", "but he also helped his teammates."], "D",
              "'Not only' pairs with 'but also', adding another positive point."),
            q("The evidence was so ___ that the jury reached a verdict within minutes.", ["weak", "overwhelming", "unclear", "irrelevant"], "B",
              "A quick verdict suggests the evidence was overwhelming."),
            q("Despite repeated warnings, ___", ["he continued to drive without a seatbelt.", "he followed every rule.",
              "he was very careful.", "the warnings worked."], "A", "'Despite' signals that he ignored the warnings."),
        ],
    ),
]
