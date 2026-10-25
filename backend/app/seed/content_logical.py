"""Qualitative Aptitude (Logical Reasoning): original lessons and questions."""

from app.seed.builders import ex, q, rule, topic

STD = ["Only I follows", "Only II follows", "Both I and II follow", "Neither I nor II follows"]
EITHER = ["Only I follows", "Only II follows", "Either I or II follows", "Neither I nor II follows"]

LOGICAL_TOPICS = [
    topic(
        "blood-relations",
        "Blood Relations",
        "Work out how people in a family are related from indirect clues.",
        """
Blood relation questions describe a family in a roundabout way ("my grandfather's only son") and ask you to name a relationship. The trick is never to hold the family in your head. Draw it.

Use a simple family tree. Write each person once. Mark males with + and females with −. Put a horizontal line between brothers and sisters, a double line between husband and wife, and a vertical line from parents down to children. Every generation sits on its own row, so grandparents are two rows above grandchildren.

Read the sentence from the end and work backwards to the speaker. "The son of my grandfather's only son": the speaker's grandfather's only son is the speaker's father, and the son of the speaker's father is the speaker's brother (or the speaker himself, if the speaker is male and nothing else rules it out).

Watch out for gender. Many questions hinge on whether a name belongs to a man or a woman, and some deliberately leave it unknown. If the gender of the person you're asked about can't be fixed, the answer may be "cannot be determined".
""",
        [
            "Draw a tree instead of reasoning in your head.",
            "Decode phrases from the end back to the speaker.",
            "Each generation goes on its own row.",
            "Note gender only when the clue actually tells you.",
        ],
        [
            rule("Father's or mother's son", "Brother (or the speaker, if male)"),
            rule("Father's sister / mother's sister", "Paternal aunt / maternal aunt"),
            rule("Mother's brother", "Maternal uncle"),
            rule("Brother's or sister's son / daughter", "Nephew / niece"),
            rule("Son's wife / daughter's husband", "Daughter-in-law / son-in-law"),
            rule("Only son of paternal grandfather", "Father"),
        ],
        [
            "\"Only daughter of my mother\", said by a woman, is the speaker herself.",
            "Coded relations (A + B means A is the father of B) are just the same tree with symbols. Translate each symbol one step at a time.",
        ],
        [
            ex(
                "Pointing to a man, Riya says, \"He is the son of my grandfather's only son.\" How is the man related to Riya?",
                [
                    "Riya's grandfather's only son is Riya's father.",
                    "The son of Riya's father is Riya's brother.",
                    "Riya is female, so the man cannot be Riya herself.",
                ],
                "He is Riya's brother.",
            ),
            ex(
                "A is B's sister. C is B's mother. D is C's father. E is D's mother. How is A related to D?",
                [
                    "A and B are siblings, and C is B's mother, so C is also A's mother.",
                    "D is C's father, so D is A's grandfather.",
                    "A is female (a sister), so A is D's granddaughter.",
                ],
                "A is D's granddaughter.",
            ),
        ],
        [
            q(
                "Introducing a woman, Arun says, \"She is the wife of the only son of my father.\" How is the woman related to Arun?",
                ["Sister", "Wife", "Mother", "Sister-in-law"],
                "B",
                "The only son of Arun's father is Arun himself (Arun is a man). So the woman is Arun's wife.",
                "easy",
            ),
            q(
                "P is the brother of Q. R is the sister of Q. S is the father of R. How is P related to S?",
                ["Son", "Brother", "Nephew", "Father"],
                "A",
                "P, Q and R are siblings. S is R's father, so S is P's father too, and P (a brother) is S's son.",
                "easy",
            ),
            q(
                "Kiran's mother is the only daughter of Vimal's father. Vimal is a man. How is Vimal related to Kiran?",
                ["Father", "Maternal uncle", "Brother", "Grandfather"],
                "B",
                "The only daughter of Vimal's father is Vimal's sister (Vimal is male, so not himself). She is Kiran's mother, so Vimal is Kiran's mother's brother: the maternal uncle.",
            ),
            q(
                "If A + B means A is the father of B and A × B means A is the brother of B, how is P related to R in P + Q × R?",
                ["Uncle", "Father", "Brother", "Grandfather"],
                "B",
                "P + Q: P is Q's father. Q × R: Q is R's brother. Siblings share a father, so P is R's father.",
            ),
        ],
        [
            q(
                "Pointing to a photograph, Meera says, \"His mother is the only daughter of my mother.\" How is Meera related to the man in the photograph?",
                ["Sister", "Aunt", "Mother", "Grandmother"],
                "C",
                "The only daughter of Meera's mother is Meera herself. So Meera is the man's mother.",
            ),
            q(
                "A is the son of B. C is B's sister and has a son D. How is A related to D?",
                ["Brother", "Cousin", "Nephew", "Uncle"],
                "B",
                "A's parent B and D's parent C are siblings. Children of siblings are cousins.",
                "easy",
            ),
            q(
                "X is the husband of Y. W is the daughter of X and Y. Z is the husband of W. N is the daughter of Z and W. How is N related to Y?",
                ["Granddaughter", "Daughter", "Niece", "Cousin"],
                "A",
                "W is Y's daughter, and N is W's daughter. So N is Y's granddaughter.",
            ),
            q(
                "Rahul's father is the brother of Neha's mother. How is Neha related to Rahul?",
                ["Sister", "Niece", "Cousin", "Aunt"],
                "C",
                "Neha's mother is the sister of Rahul's father. So their parents are siblings and Neha is Rahul's cousin.",
            ),
            q(
                "A $ B means A is the mother of B, A # B means A is the sister of B, and A @ B means A is the father of B. Which expression shows that P is the grandmother of S?",
                ["P $ Q @ S", "P # Q $ S", "P @ Q $ S", "P $ Q # S"],
                "A",
                "P $ Q @ S: P is Q's mother and Q is S's father, so P is S's paternal grandmother. B makes P an aunt, C a grandfather, and D makes P the mother of S.",
                "hard",
            ),
            q(
                "In a family of six (A, B, C, D, E, F) there are two married couples. B is the mother of D. A is the father of C. D is the sister of C. E is the wife of C, and F is the son of E. How is A related to F?",
                ["Father", "Uncle", "Grandfather", "Great-grandfather"],
                "C",
                "C and D are siblings, so A and B are their parents (first couple). C and E are the second couple, and F is their son. A is C's father, so A is F's grandfather.",
                "hard",
            ),
        ],
    ),
    topic(
        "coding-decoding",
        "Coding and Decoding",
        "Crack the rule that turns a word or number into a code.",
        """
In coding–decoding, a word is converted into a code using a hidden rule, and you apply the same rule to a new word. Placement tests use a small set of rules again and again, so the fastest way to improve is to recognise them on sight.

The most common rules are: shifting each letter forward or backward by a fixed number; shifting by a changing amount (+1, +2, +3…); replacing each letter with its "opposite" letter (A↔Z, B↔Y); reversing the word; and replacing letters with their position numbers (A = 1 … Z = 26).

Always write the alphabet positions down while practising. Knowing EJOTY (E = 5, J = 10, O = 15, T = 20, Y = 25) lets you find any letter's position in a second.

Sentence codes ("sky is blue" → "ta na ro") work differently: compare two sentences, and the word they share gets the code they share.
""",
        [
            "Write the position of each letter above the word and the code below it.",
            "Check the difference between matching letters: constant, increasing, or opposite.",
            "For sentence codes, find words common to two sentences.",
        ],
        [
            rule("Letter positions", "A=1, B=2 … Z=26", "Memorise EJOTY: 5, 10, 15, 20, 25"),
            rule("Opposite letter", "position + opposite position = 27", "A↔Z, B↔Y, M↔N"),
            rule("Forward shift past Z", "wrap around: Y + 3 = B"),
        ],
        [
            "If the code has the same number of letters as the word, look for a letter-by-letter rule first.",
            "If the code looks like the word backwards, check reversal before anything else.",
        ],
        [
            ex(
                "If CAT is coded as DBU, how is DOG coded?",
                ["C→D, A→B, T→U: every letter moves 1 forward.", "D→E, O→P, G→H."],
                "EPH",
            ),
            ex(
                "In a code, MOBILE is written as NLYROV. How is PHONE written?",
                [
                    "M(13)→N(14), O(15)→L(12), B(2)→Y(25): each pair adds up to 27, so every letter becomes its opposite.",
                    "P(16)→K(11), H(8)→S(19), O(15)→L(12), N(14)→M(13), E(5)→V(22).",
                ],
                "KSLMV",
            ),
        ],
        [
            q("If TABLE is coded as UBCMF, how is CHAIR coded?", ["DIBJS", "BGZHQ", "DIBKS", "EJCKT"], "A",
              "Each letter moves one place forward: C→D, H→I, A→B, I→J, R→S.", "easy"),
            q("In a code, each letter is replaced by the letter two places before it. How is GOAL coded?",
              ["EMYJ", "IQCN", "EMZJ", "FNZK"], "A",
              "G→E, O→M, A→Y (wrapping around), L→J.", "easy"),
            q("If A = 1, B = 2 and so on, and BAD is coded as 7 (2 + 1 + 4), what is the code for FACE?",
              ["14", "15", "16", "13"], "B",
              "F(6) + A(1) + C(3) + E(5) = 15."),
            q("In a code, 'sky is blue' is written as 'ta na ro' and 'blue is good' is written as 'na ro mi'. What is the code for 'sky'?",
              ["ta", "na", "ro", "mi"], "A",
              "'is' and 'blue' appear in both sentences, so they are 'na' and 'ro'. The remaining word 'sky' is 'ta'."),
        ],
        [
            q("If PLANET is coded as TENALP, how is ORANGE coded?", ["EGNARO", "EGANRO", "OGNARE", "EGNRAO"], "A",
              "The code is the word written backwards. ORANGE reversed is EGNARO.", "easy"),
            q("If each letter in WORD is replaced by its opposite letter (A↔Z, B↔Y …), what does WORD become?",
              ["DLIW", "DLJW", "ELIW", "DMIW"], "A",
              "W(23)↔D(4), O(15)↔L(12), R(18)↔I(9), D(4)↔W(23). Each pair adds to 27."),
            q("If MANGO is coded as 13-1-14-7-15, what is the code for LEMON?",
              ["12-5-13-15-14", "12-5-13-14-15", "11-5-13-15-14", "12-6-13-15-14"], "A",
              "Each letter becomes its position: L = 12, E = 5, M = 13, O = 15, N = 14."),
            q("In a code, FRIEND is written as HUMJTK. How is CANDLE written?", ["EDRIRL", "EDRJRL", "DCQHQK", "EDRIQL"], "A",
              "The shifts are +2, +3, +4, +5, +6, +7 (F→H, R→U, I→M, E→J, N→T, D→K). CANDLE: C+2 = E, A+3 = D, N+4 = R, D+5 = I, L+6 = R, E+7 = L.",
              "hard"),
            q("'pit nat sa' means 'you are good', 'sa tik rot' means 'good and bad', and 'nat lu rot' means 'are they bad'. Which word means 'good'?",
              ["sa", "nat", "rot", "tik"], "A",
              "'good' appears in the first two sentences, and the only code common to both is 'sa'."),
            q("If ROSE is coded as 6821, CHAIR as 73456 and PREACH as 961473, what is the code for SEARCH?",
              ["214673", "214763", "216473", "241673"], "A",
              "From the examples: S = 2, E = 1, A = 4, R = 6, C = 7, H = 3. SEARCH = 2 1 4 6 7 3.", "hard"),
        ],
    ),
    topic(
        "number-letter-series",
        "Number and Letter Series",
        "Find the rule behind a sequence and predict the next term.",
        """
A series is a list of numbers or letters that follows a rule. Your job is to find the rule and continue it, or to spot the term that breaks it.

Start with the differences between neighbouring terms. If the differences are constant, it's an arithmetic series. If the differences themselves change steadily (4, 6, 8, 10), look at the second differences. If the terms grow very fast, try ratios (×2, ×3) or a mixed rule like ×2 + 1.

Also keep a short list of famous sequences in your head: squares (1, 4, 9, 16 …), cubes (1, 8, 27, 64 …), primes (2, 3, 5, 7, 11 …), and "square ± 1" patterns. Some series alternate between two rules: odd positions follow one pattern, even positions another.

For letter series, convert each letter to its position number and treat it exactly like a number series.
""",
        [
            "Try differences first, then ratios, then known sequences.",
            "If the pattern breaks every other term, split the series into odd and even positions.",
            "Turn letters into numbers (A = 1 … Z = 26).",
        ],
        [
            rule("Arithmetic series", "next = previous + d"),
            rule("Geometric series", "next = previous × r"),
            rule("n(n + 1) pattern", "2, 6, 12, 20, 30 …"),
            rule("Square ± 1", "n² − 1: 3, 8, 15, 24 …"),
        ],
        [
            "When the numbers jump a lot, check ×2, ×3 or ×n + k before trying differences.",
            "In 'find the wrong term' questions, test each term against the rule. Exactly one will fail.",
        ],
        [
            ex("Find the next term: 2, 6, 12, 20, 30, ?",
               ["Differences: 4, 6, 8, 10, rising by 2.", "Next difference is 12, so 30 + 12 = 42.", "Also 1×2, 2×3, 3×4 … 6×7 = 42."],
               "42"),
            ex("Find the next letter: B, E, H, K, ?",
               ["Positions: 2, 5, 8, 11. Each step adds 3.", "11 + 3 = 14, which is N."],
               "N"),
        ],
        [
            q("3, 9, 27, 81, ?", ["162", "243", "324", "729"], "B", "Each term is multiplied by 3: 81 × 3 = 243.", "easy"),
            q("1, 4, 9, 16, 25, ?", ["30", "35", "36", "49"], "C", "These are squares 1², 2², 3² … The next is 6² = 36.", "easy"),
            q("A, C, F, J, O, ?", ["T", "U", "V", "S"], "B",
              "Positions 1, 3, 6, 10, 15 increase by 2, 3, 4, 5, so add 6: 21 = U."),
            q("5, 11, 23, 47, ?", ["94", "95", "96", "97"], "B", "Each term is ×2 + 1: 47 × 2 + 1 = 95."),
        ],
        [
            q("7, 10, 16, 25, 37, ?", ["48", "50", "52", "54"], "C", "Differences are 3, 6, 9, 12, so the next is 15: 37 + 15 = 52."),
            q("2, 3, 5, 7, 11, 13, ?", ["15", "16", "17", "19"], "C", "Consecutive prime numbers. The prime after 13 is 17.", "easy"),
            q("120, 99, 80, 63, 48, ?", ["35", "36", "33", "39"], "A",
              "Each term is a square minus 1: 11² − 1, 10² − 1 … 7² − 1. Next is 6² − 1 = 35."),
            q("Z, X, U, Q, L, ?", ["G", "F", "E", "H"], "B",
              "Positions 26, 24, 21, 17, 12 fall by 2, 3, 4, 5, so subtract 6: 6 = F."),
            q("4, 8, 6, 12, 10, 20, ?", ["18", "22", "40", "16"], "A",
              "The rule alternates ×2 and −2: 4×2 = 8, 8−2 = 6, 6×2 = 12, 12−2 = 10, 10×2 = 20, 20−2 = 18."),
            q("Find the wrong number: 2, 5, 10, 17, 26, 38, 50", ["17", "26", "38", "50"], "C",
              "The series is n² + 1: 2, 5, 10, 17, 26, 37, 50. The sixth term should be 37, not 38.", "hard"),
        ],
    ),
    topic(
        "direction-sense",
        "Direction Sense",
        "Track movements and turns to find final position and distance.",
        """
Direction questions describe someone walking and turning, then ask where they end up or how far they are from the start. Draw a quick sketch with North at the top, East on the right.

Turning right is a clockwise turn of 90°; turning left is anticlockwise. To keep turns straight, ask "which way am I facing now?" after every step. If you face south and turn left, you now face east.

For distance, track total east–west movement and total north–south movement separately. The straight-line distance is then found with Pythagoras: √(x² + y²). The common right triangles 3-4-5, 6-8-10 and 5-12-13 appear constantly.

Shadow questions use one fact: the sun rises in the east and sets in the west. In the morning, shadows fall towards the west; in the evening, towards the east.
""",
        [
            "Sketch with North up and East right.",
            "Update the facing direction after every turn.",
            "Add up east–west and north–south moves separately.",
            "Morning shadow → west. Evening shadow → east.",
        ],
        [
            rule("Shortest distance", "√(x² + y²)", "x = net east–west, y = net north–south"),
            rule("Right turn", "90° clockwise"),
            rule("Left turn", "90° anticlockwise"),
            rule("Clockwise order", "N → NE → E → SE → S → SW → W → NW"),
        ],
        [
            "Moves in opposite directions cancel: 5 km east then 2 km west is 3 km east.",
            "For angle turns, add clockwise angles and subtract anticlockwise ones, then count in 45° steps.",
        ],
        [
            ex("Ravi walks 4 km north, turns right and walks 3 km. How far is he from the start, and in which direction?",
               ["Facing north, a right turn faces east. Ravi is 4 km north and 3 km east.", "Distance = √(4² + 3²) = √25 = 5 km.",
                "North and east together give north-east."],
               "5 km to the north-east"),
            ex("Sita faces east. She turns 90° anticlockwise, then 135° clockwise. Which way does she face now?",
               ["Net turn = 135° clockwise − 90° anticlockwise = 45° clockwise.", "45° clockwise from east is south-east."],
               "South-east"),
        ],
        [
            q("A man walks 5 km south, turns left and walks 5 km. In which direction is he from his starting point?",
              ["North-East", "South-East", "South-West", "North-West"], "B",
              "Facing south, a left turn faces east. He is south and east of the start: south-east.", "easy"),
            q("Priya walks 6 m north, then 8 m east. How far is she from the starting point?",
              ["14 m", "10 m", "12 m", "2 m"], "B", "√(6² + 8²) = √100 = 10 m.", "easy"),
            q("You face west and turn 90° clockwise. Which direction do you face now?", ["North", "South", "East", "West"], "A",
              "Clockwise from west is north.", "easy"),
            q("One morning after sunrise, Kavi stands facing a pole. The pole's shadow falls exactly to his right. Which direction is he facing?",
              ["North", "South", "East", "West"], "B",
              "In the morning the sun is in the east, so shadows fall west. West is on his right, so he faces south."),
        ],
        [
            q("A car travels 10 km west, turns right and travels 6 km, then turns right again and travels 10 km. Where is it now relative to the start?",
              ["6 km North", "6 km South", "16 km North", "10 km East"], "A",
              "West 10, then right (north) 6, then right (east) 10. The east and west moves cancel, leaving 6 km north."),
            q("Arjun walks 3 km east, then 4 km north, then 3 km west. How far is he from his starting point?",
              ["4 km", "10 km", "7 km", "5 km"], "A", "The east and west moves cancel. He is 4 km north of the start.", "easy"),
            q("Facing south-west, Leena turns 90° anticlockwise. Which direction is she facing now?",
              ["North-West", "South-East", "North-East", "South"], "B",
              "Anticlockwise from south-west: 45° gives south, 90° gives south-east."),
            q("A man walks 2 km north, turns east and walks 5 km, turns south and walks 6 km, then turns west and walks 2 km. How far is he from the start?",
              ["5 km", "3 km", "4 km", "7 km"], "A",
              "Net east = 5 − 2 = 3 km. Net south = 6 − 2 = 4 km. Distance = √(3² + 4²) = 5 km.", "hard"),
            q("In the evening, two friends stand facing each other. The first friend's shadow falls exactly to his left. Which direction is the second friend facing?",
              ["North", "South", "East", "West"], "B",
              "Evening shadows fall east. East is on the first friend's left, so he faces north. The second friend faces him, so faces south.",
              "hard"),
            q("B is 8 m east of A. C is 6 m north of B. D is 8 m west of C. Where is D relative to A?",
              ["6 m North", "8 m North", "10 m North-East", "6 m South"], "A",
              "The 8 m east and 8 m west cancel. D is directly 6 m north of A."),
        ],
    ),
    topic(
        "seating-arrangements",
        "Seating Arrangements",
        "Place people in rows or around tables from a set of clues.",
        """
Seating questions give clues about where people sit and ask you to deduce the full arrangement. They come in two shapes: a straight row, and a circle (or square) around a table.

In a row, first fix which way everyone faces, because "left" and "right" are always from the person's own point of view. If people face north, their left is your left as you look at the page; if they face south, it flips.

Around a table where everyone faces the centre, a person's right is the anticlockwise neighbour and their left is the clockwise neighbour. Number the seats clockwise, place one person, and build outwards from them.

Always place the definite clues first (ends, opposite seats, "immediate" neighbours) and leave vague clues ("somewhere to the left") for last. If two arrangements still fit, use the remaining clue to choose between them.
""",
        [
            "Fix the facing direction before reading left/right.",
            "Number circular seats clockwise and anchor one person.",
            "Use definite clues first, vague clues last.",
        ],
        [
            rule("Facing the centre", "right = anticlockwise neighbour, left = clockwise neighbour"),
            rule("Position from both ends", "total = position from left + position from right − 1"),
            rule("Opposite seat (n people)", "seat number + n/2"),
        ],
        [
            "If X is to the immediate left of Y (both facing the centre), then Y is to the immediate right of X.",
            "When two people swap places, use the position of the other person to find the total.",
        ],
        [
            ex("Five friends A, B, C, D and E sit in a row facing north. C is in the middle. A is to the immediate left of C. B is at the right end. E is to the left of A. Who sits between C and B?",
               ["Number seats 1 to 5 from the left. C is in seat 3.", "A is in seat 2, B in seat 5.",
                "E is left of A, so E is in seat 1. D takes the remaining seat 4.", "Seat 4 is between C (3) and B (5)."],
               "D"),
            ex("P, Q, R, S, T and U sit around a circular table facing the centre. P is opposite S. Q is to the immediate right of P. R is opposite Q. T sits between P and R. Who is to the immediate left of S?",
               ["Number seats 1–6 clockwise. Put P in seat 1, so S (opposite) is seat 4.",
                "Facing the centre, P's right is the anticlockwise seat: Q is seat 6. R, opposite Q, is seat 3.",
                "T is between P (1) and R (3), so T is seat 2. U takes seat 5.",
                "S's left is the clockwise neighbour, seat 5."],
               "U"),
        ],
        [
            q("A, B, C, D and E sit in a row facing north. B is at the extreme left. D is second to the right of B. E is to the immediate right of D. C is between B and D. Who is at the extreme right?",
              ["A", "C", "D", "E"], "A",
              "B is in seat 1, D in seat 3, E in seat 4, C in seat 2, which leaves A in seat 5 at the right end."),
            q("Ram, Shyam, Mohan and Gopal sit around a square table, one on each side, facing the centre. Ram is opposite Shyam. Mohan is to the immediate right of Ram. Who is to the immediate left of Ram?",
              ["Shyam", "Mohan", "Gopal", "Cannot be determined"], "C",
              "Ram's opposite is Shyam and his right is Mohan, so the remaining seat on his left belongs to Gopal.", "easy"),
            q("In a row of 7 students facing north, Neha is fourth from the left. Ravi is to the immediate right of Neha. What is Ravi's position from the right end?",
              ["2nd", "3rd", "4th", "5th"], "B", "Ravi is 5th from the left in a row of 7, so 7 − 5 + 1 = 3rd from the right.", "easy"),
            q("Five people sit around a circular table facing the centre. Kiran is to the immediate left of Lata. Mira is to the immediate left of Kiran. Who is to the immediate right of Kiran?",
              ["Mira", "Lata", "Cannot be determined", "Kiran"], "B",
              "If Kiran is to Lata's immediate left, then Lata is to Kiran's immediate right."),
        ],
        [
            q("Six students sit in a row facing north. P is second from the left end. Q is to the immediate right of P. R is at the right end. S is to the immediate left of R. T is to the left of P. Who sits between Q and S?",
              ["T", "U", "R", "P"], "B",
              "Seats from the left: T 1, P 2, Q 3, S 5, R 6. The only person left, U, takes seat 4, between Q and S."),
            q("Six friends sit around a circular table facing the centre. Ajay is opposite Bina. Chetan is to the immediate right of Ajay. Divya is to the immediate left of Bina. Farhan sits next to Bina. Esha is the sixth friend. Who is to the immediate left of Ajay?",
              ["Chetan", "Esha", "Farhan", "Divya"], "B",
              "Seats clockwise: Ajay 1, Bina 4. Ajay's right (anticlockwise) is seat 6, Chetan. Bina's left (clockwise) is seat 5, Divya. Farhan is next to Bina, so seat 3. Esha takes seat 2, which is Ajay's left.",
              "hard"),
            q("A, B, C, D and E sit in a row facing south. A is at the extreme left end. C is to the immediate right of A. E is in the middle. B is not next to E. Who is to the immediate right of E?",
              ["C", "D", "B", "A"], "B",
              "Counting from their own left: A 1, C 2, E 3. B is not next to E, so B is 5 and D is 4. E's immediate right is D."),
            q("Seven students sit in a row facing north. Mona is fifth from the right end and Sonu is second from the left end. How many students sit between them?",
              ["0", "1", "2", "3"], "A", "Mona is 7 − 5 + 1 = 3rd from the left; Sonu is 2nd. They sit side by side."),
            q("L, M, N, O, P and Q sit around a circular table facing the centre. L is opposite O. M is to the immediate left of L. N is to the immediate right of O. P is next to O but not next to L. Who is opposite M?",
              ["N", "P", "Q", "O"], "B",
              "Seats clockwise: L 1, O 4. M is L's left (clockwise): seat 2. N is O's right (anticlockwise): seat 3. P is next to O, so seat 5, and Q is seat 6. Opposite M (2) is seat 5: P.",
              "hard"),
            q("In a row facing north, X is 9th from the left and Y is 12th from the right. When they swap places, X becomes 15th from the left. How many people are in the row?",
              ["25", "26", "27", "28"], "B",
              "After the swap X is in Y's old seat, so Y's seat is 15th from the left and 12th from the right. Total = 15 + 12 − 1 = 26.",
              "hard"),
        ],
    ),
    topic(
        "syllogisms",
        "Syllogisms",
        "Decide which conclusions must follow from given statements.",
        """
A syllogism gives two or more statements and asks which conclusions definitely follow. Treat the statements as true even if they sound silly in real life ("All birds are cats"). Your only job is logic.

Statements use four forms: All A are B, Some A are B, No A is B, and Some A are not B. Draw each as a Venn diagram. A conclusion follows only if it is true in every possible diagram, not just the first one you draw.

Useful facts: "All A are B" also gives "Some B are A". "No A is B" works both ways (No B is A). Two "Some" statements never give a definite conclusion between their outer terms.

Watch for complementary pairs. If two conclusions are about the same two terms and one is "Some A are B" while the other is "No A is B" (or "All" with "Some … not"), exactly one of them must be true. When neither follows on its own, the answer is "Either I or II follows".
""",
        [
            "Accept the statements as true, whatever the real world says.",
            "A conclusion must hold in every possible diagram.",
            "Check for an either-or (complementary) pair when neither follows alone.",
        ],
        [
            rule("All + All", "All A are B, All B are C ⇒ All A are C"),
            rule("All + No", "All A are B, No B is C ⇒ No A is C"),
            rule("Some + All", "Some A are B, All B are C ⇒ Some A are C"),
            rule("Conversion", "All A are B ⇒ Some B are A;  No A is B ⇒ No B is A"),
            rule("Some + Some", "no definite conclusion"),
        ],
        [
            "\"All A are B\" never gives \"All B are A\".",
            "Complementary pairs: Some/No, All/Some-not, about the same two terms.",
        ],
        [
            ex("Statements: All pens are books. All books are bags. Conclusions: I. All pens are bags. II. Some bags are pens.",
               ["All + All: pens sit inside books, which sit inside bags, so all pens are bags. I follows.",
                "Since all pens are bags, some bags must be pens. II follows."],
               "Both I and II follow"),
            ex("Statements: Some cats are dogs. No dog is a rat. Conclusions: I. Some cats are not rats. II. No cat is a rat.",
               ["The cats that are dogs cannot be rats, so some cats are definitely not rats. I follows.",
                "Other cats might still be rats, so II is not certain."],
               "Only I follows"),
        ],
        [
            q("Statements: All roses are flowers. All flowers are plants. Conclusions: I. All roses are plants. II. All plants are roses.",
              STD, "A", "All + All gives 'All roses are plants'. The reverse ('All plants are roses') is not implied.", "easy"),
            q("Statements: No apple is a mango. All mangoes are fruits. Conclusions: I. Some fruits are not apples. II. No fruit is an apple.",
              STD, "A", "The mangoes are fruits and are not apples, so some fruits are not apples. Other fruits might be apples, so II is not certain."),
            q("Statements: Some students are singers. Some singers are dancers. Conclusions: I. Some students are dancers. II. No student is a dancer.",
              EITHER, "C",
              "Some + Some gives no definite link between students and dancers. But I and II are a complementary pair (Some/No) about the same terms, so one of them must be true."),
            q("Statements: All teachers are graduates. Some graduates are engineers. Conclusions: I. Some teachers are engineers. II. Some graduates are teachers.",
              STD, "B", "'All teachers are graduates' converts to 'Some graduates are teachers', so II follows. Teachers may or may not be among the engineers, so I is not certain."),
        ],
        [
            q("Statements: All chairs are tables. No table is a pen. Conclusions: I. No chair is a pen. II. Some tables are chairs.",
              STD, "C", "All + No gives 'No chair is a pen'. 'All chairs are tables' converts to 'Some tables are chairs'. Both follow."),
            q("Statements: Some boxes are cartons. All cartons are crates. Conclusions: I. Some boxes are crates. II. All crates are boxes.",
              STD, "A", "Some + All gives 'Some boxes are crates'. Nothing says every crate is a box."),
            q("Statements: No car is a bus. No bus is a train. Conclusions: I. No car is a train. II. Some cars are trains.",
              EITHER, "C", "Two negative statements give no definite conclusion, but I and II form a complementary pair (No/Some) about cars and trains, so one must be true."),
            q("Statements: All doctors are intelligent. Some intelligent people are rich. Conclusions: I. Some doctors are rich. II. All rich people are doctors.",
              STD, "D", "The rich intelligent people may or may not include doctors, so I is not certain. II has no support at all."),
            q("Statements: All birds can fly. Some birds are parrots. Conclusions: I. Some parrots can fly. II. All parrots are birds.",
              STD, "A", "The parrots that are birds can fly, so some parrots can fly. We only know some parrots are birds, so II does not follow.", "hard"),
            q("Statements: Some pencils are erasers. All erasers are sharpeners. No sharpener is a scale. Conclusions: I. Some pencils are not scales. II. Some erasers are scales.",
              STD, "A", "Pencils that are erasers are sharpeners, and no sharpener is a scale, so those pencils are not scales: I follows. All erasers are sharpeners, so no eraser is a scale: II is false.", "hard"),
        ],
    ),
    topic(
        "analogies",
        "Analogies",
        "Spot the relationship in one pair and apply it to another.",
        """
An analogy question shows a pair of words, numbers or letters with a hidden relationship, then asks you to complete a second pair with the same relationship. Write A : B :: C : ? as "A is to B as C is to ?".

Say the relationship in a full sentence: "A doctor uses a stethoscope." Then test each option in the same sentence: "A carpenter uses a … saw." The option that fits the sentence exactly is the answer. If more than one fits, make your sentence more specific.

Common relationships: worker and tool, worker and workplace, tool and function, raw material and product, part and whole, animal and its home or group, cause and effect, synonyms and antonyms, and instrument and what it measures.

Number analogies usually use squares, cubes, multiples or a simple formula like n² + 1. Letter analogies usually shift every letter by the same amount.
""",
        [
            "Turn the first pair into a precise sentence.",
            "Plug each option into the same sentence.",
            "For numbers, test square, cube and ×k first.",
        ],
        [
            rule("Worker : Tool", "Doctor : Stethoscope"),
            rule("Instrument : Measures", "Thermometer : Temperature"),
            rule("Raw material : Product", "Cotton : Cloth"),
            rule("Animal : Group", "Lion : Pride, Fish : School"),
            rule("Number pairs", "n : n², n : n³, n : n² + 1"),
        ],
        [
            "The order matters: Cloth : Cotton is not the same as Cotton : Cloth.",
            "Eliminate options from the same category as C but with a different relationship.",
        ],
        [
            ex("Doctor : Stethoscope :: Carpenter : ?",
               ["Relationship: a doctor uses a stethoscope as a tool of the trade.", "A carpenter's tool is a saw."],
               "Saw"),
            ex("3 : 27 :: 5 : ?", ["27 = 3³.", "So the answer is 5³ = 125."], "125"),
        ],
        [
            q("Book : Author :: Painting : ?", ["Canvas", "Painter", "Brush", "Gallery"], "B", "An author creates a book; a painter creates a painting.", "easy"),
            q("Bird : Nest :: Bee : ?", ["Hive", "Den", "Stable", "Burrow"], "A", "A bird lives in a nest; a bee lives in a hive.", "easy"),
            q("4 : 16 :: 7 : ?", ["28", "42", "49", "56"], "C", "16 = 4². So 7² = 49.", "easy"),
            q("ACE : BDF :: GIK : ?", ["HJL", "HIJ", "IKM", "GHI"], "A", "Each letter moves forward by 1: G→H, I→J, K→L."),
        ],
        [
            q("Thermometer : Temperature :: Barometer : ?", ["Humidity", "Pressure", "Rainfall", "Wind speed"], "B",
              "A thermometer measures temperature; a barometer measures atmospheric pressure."),
            q("Cotton : Cloth :: Clay : ?", ["Brick", "Mud", "Potter", "Kiln"], "A",
              "Cotton is the raw material for cloth; clay is the raw material for bricks."),
            q("Lion : Pride :: Fish : ?", ["Herd", "Flock", "School", "Pack"], "C", "A group of lions is a pride; a group of fish is a school."),
            q("8 : 64 :: 11 : ?", ["111", "121", "132", "99"], "B", "64 = 8², so 11² = 121.", "easy"),
            q("Pen : Write :: Knife : ?", ["Sharp", "Cut", "Kitchen", "Steel"], "B", "A pen is used to write; a knife is used to cut.", "easy"),
            q("BDFH : CEGI :: JLNP : ?", ["KMOQ", "KLMN", "JKLM", "LNPR"], "A", "Each letter moves forward by 1: J→K, L→M, N→O, P→Q."),
        ],
    ),
    topic(
        "logical-puzzles",
        "Logical Puzzles",
        "Solve ranking, matching and truth-teller puzzles step by step.",
        """
Puzzles give you a handful of clues about people and their attributes (height, rank, job, day) and ask you to deduce one fact. They look long, but they follow a method.

For ranking puzzles, turn every clue into a symbol: "A is taller than B" becomes A > B. Chain the symbols into one line, and the order falls out.

For matching puzzles (who likes which fruit, who has which job), draw a grid with people in rows and options in columns. Put ✗ where a clue rules something out and ✓ where it confirms it. When a row has only one empty cell, it must be ✓. That ✓ then rules the same option out for everyone else.

For truth-teller puzzles, assume one person tells the truth and follow the consequences. If you reach a contradiction, the assumption was wrong. Try the next.
""",
        [
            "Turn comparisons into a chain: A > B > C.",
            "Use a grid for matching puzzles and fill in ✗ and ✓.",
            "For liars and truth-tellers, test each assumption until there's no contradiction.",
        ],
        [
            rule("Rank from both ends", "total = rank from top + rank from bottom − 1"),
            rule("Position after a gap", "position = first position + people between + 1"),
        ],
        [
            "Write the strongest clue (a fixed position, 'first', 'last') before anything else.",
            "If a question asks 'who can't be determined', look for a person whose position two arrangements disagree on.",
        ],
        [
            ex("Among A, B, C, D and E, A is taller than B but shorter than C. D is taller than C. E is the shortest. Who is the second tallest?",
               ["C > A > B from the first clue.", "D > C, so D > C > A > B.", "E is shortest: D > C > A > B > E."],
               "C"),
            ex("Anu, Bala and Chitra each like a different fruit: apple, mango or banana. Anu likes neither mango nor banana. Bala doesn't like mango. Who likes mango?",
               ["Anu must like apple.", "Bala doesn't like mango, and apple is taken, so Bala likes banana.", "That leaves mango for Chitra."],
               "Chitra"),
        ],
        [
            q("P is older than Q. R is older than P. S is younger than Q. Who is the youngest?", ["P", "Q", "R", "S"], "D",
              "R > P > Q > S, so S is the youngest.", "easy"),
            q("In a class, Raj is 7th from the top and 18th from the bottom. How many students are in the class?",
              ["24", "25", "23", "26"], "A", "Total = 7 + 18 − 1 = 24.", "easy"),
            q("Three boxes are labelled 'Apples', 'Oranges' and 'Mixed', and every label is wrong. A fruit taken from the box labelled 'Mixed' is an apple. What does the box labelled 'Oranges' contain?",
              ["Apples", "Oranges", "Mixed", "Cannot be determined"], "C",
              "The 'Mixed' box can't be mixed, and it has an apple, so it holds only apples. The 'Oranges' box can't hold oranges, and apples are taken, so it holds the mixed fruit.",
              "hard"),
            q("Five books are stacked. Biology is at the top. Maths is above Physics. Chemistry is below Physics. English is between Physics and Chemistry. Which book is in the middle?",
              ["Maths", "Physics", "English", "Chemistry"], "B",
              "From the top: Biology, Maths, Physics, English, Chemistry. The third (middle) book is Physics."),
        ],
        [
            q("Mohan scored more than Sohan but less than Rohan. Jay scored more than Rohan. Vijay scored the least. Who scored the second highest?",
              ["Mohan", "Rohan", "Jay", "Sohan"], "B", "Jay > Rohan > Mohan > Sohan > Vijay. Rohan is second."),
            q("W, X, Y and Z have different jobs: doctor, lawyer, teacher and engineer. W is neither a doctor nor a lawyer. X is the teacher. Y is not the doctor. What is Z's job?",
              ["Doctor", "Lawyer", "Engineer", "Teacher"], "A",
              "X is the teacher, so W must be the engineer. Y isn't the doctor, so Y is the lawyer. Z is the doctor."),
            q("In a queue, Asha is 10th from the front and Ritu is 15th from the back. There are 4 people between them, and Asha is ahead of Ritu. How many people are in the queue?",
              ["29", "28", "30", "27"], "A",
              "Ritu is 10 + 4 + 1 = 15th from the front and 15th from the back. Total = 15 + 15 − 1 = 29.", "hard"),
            q("A says, 'B is lying.' B says, 'C is lying.' C says, 'A and B are both lying.' Who is telling the truth?",
              ["Only A", "Only B", "Only C", "A and C"], "B",
              "If A tells the truth, B lies, so C tells the truth, but then A is lying: a contradiction. So A lies, B tells the truth, and C lies (B isn't lying, so C's claim is false). Only B is truthful.",
              "hard"),
            q("Six plays are staged Monday to Saturday, one per day. K is on Wednesday. M is the day after K. L is on Monday. N is two days after M. O is not on Tuesday. Which play is on Tuesday?",
              ["O", "P", "N", "M"], "B",
              "L Monday, K Wednesday, M Thursday, N Saturday. Tuesday and Friday remain for O and P. O isn't on Tuesday, so P is."),
            q("Five people stand in a line: Farah is at the left end, Esha at the right end, Dev is immediately left of Esha, and Gaurav is immediately left of Dev. Hari is the fifth person. Who stands in the middle?",
              ["Hari", "Gaurav", "Dev", "Farah"], "B",
              "From the left: Farah 1, Hari 2, Gaurav 3, Dev 4, Esha 5. Gaurav is in the middle.", "easy"),
        ],
    ),
    topic(
        "statement-conclusion",
        "Statement and Conclusion",
        "Judge which conclusions follow directly from a statement.",
        """
Here you get a short statement, often from a notice, news item or advertisement, and two conclusions. A conclusion "follows" if it can be reasonably drawn from the statement alone, without adding outside facts or opinions.

Read the statement literally. Then ask of each conclusion: "Does the statement give me enough to say this?" A conclusion can follow even if it's not stated word for word, as long as it's the natural, direct implication. For example, "The library will be closed on Sunday" implies the library is normally open on Sundays.

Be suspicious of extreme words such as all, always, never, only, and definitely. They usually go further than the statement. Also reject conclusions that predict consequences the statement never mentions.
""",
        [
            "Use only what the statement says, plus common-sense implications.",
            "Extreme words (all, always, never, only) usually mean it doesn't follow.",
            "Two conclusions can both follow, or neither.",
        ],
        [
            rule("Follows", "Directly implied by the statement"),
            rule("Doesn't follow", "Needs extra facts, over-generalises, or predicts too much"),
        ],
        [
            "Ask: would the writer of the statement agree with this conclusion?",
            "A notice about a change implies what was normal before the change.",
        ],
        [
            ex("Statement: The government has made helmets compulsory for two-wheeler riders. Conclusions: I. Helmets reduce the risk of head injury. II. All accidents happen to two-wheeler riders.",
               ["The rule exists because helmets protect riders, so I follows.", "II is an extreme claim the statement doesn't support."],
               "Only I follows"),
            ex("Statement: 'Buy one, get one free', offer valid till Sunday. Conclusions: I. The shop wants to increase sales. II. Prices will double after Sunday.",
               ["Offers are run to boost sales, so I follows.", "Nothing suggests prices will double, so II doesn't."],
               "Only I follows"),
        ],
        [
            q("Statement: Regular exercise helps maintain good health. Conclusions: I. People who exercise regularly tend to be healthier. II. People who do not exercise always fall ill.",
              STD, "A", "I restates the statement. II uses 'always' and goes far beyond it.", "easy"),
            q("Statement: The library will remain closed on Sunday for maintenance. Conclusions: I. The library is usually open on Sunday. II. The library needs maintenance.",
              STD, "C", "Announcing a Sunday closure implies it's normally open then, and the reason given is maintenance. Both follow."),
            q("Statement: Many students in the hostel fell ill after eating at the mess. Conclusions: I. The mess food may have been contaminated. II. All hostel students will fall ill.",
              STD, "A", "I is a reasonable inference. II uses 'all' and predicts something unsupported.", "easy"),
            q("Statement: Only graduates can apply for this job. Conclusions: I. Ramesh, who has passed only class 12, cannot apply. II. All graduates will get the job.",
              STD, "A", "Ramesh isn't a graduate, so he can't apply. Being allowed to apply doesn't mean getting the job."),
        ],
        [
            q("Statement: The prices of vegetables rise every year during the monsoon. Conclusions: I. The supply of vegetables is affected during the monsoon. II. People stop eating vegetables in the monsoon.",
              STD, "A", "Rising prices suggest reduced supply. If people stopped eating vegetables, prices would fall, so II doesn't follow."),
            q("Statement: The company has announced bonuses for employees who meet their targets. Conclusions: I. Some employees may work harder to meet targets. II. Employees who miss their targets will be dismissed.",
              STD, "A", "A bonus is an incentive, so I follows. Nothing is said about dismissal."),
            q("Statement: Smoking is injurious to health. Conclusions: I. Non-smokers live forever. II. Smoking can harm health.",
              STD, "B", "II restates the statement. I is absurd and unsupported.", "easy"),
            q("Statement: The new metro line has reduced travel time between the two cities by half. Conclusions: I. The metro is faster than the earlier way of travelling. II. Earlier, the journey took twice as long.",
              STD, "C", "Halving the time means the metro is faster, and the old journey took twice as long. Both follow."),
            q("Statement: All candidates must bring their admit cards to the exam hall. Conclusions: I. Candidates without admit cards may not be allowed in. II. Admit cards are available only at the exam hall.",
              STD, "A", "If admit cards are required, entry may be refused without one. Candidates must bring them, so they aren't handed out at the hall."),
            q("Statement: Some of the city's lakes have dried up this summer. Conclusions: I. All the city's lakes have dried up. II. There was no rain at all in the city this year.",
              STD, "D", "'Some' doesn't mean 'all', and the statement gives no information about rainfall for the whole year."),
        ],
    ),
    topic(
        "critical-thinking",
        "Critical Thinking",
        "Find assumptions and judge what strengthens or weakens an argument.",
        """
Critical thinking questions give you a short argument and ask about its logic: what it assumes, what would make it stronger or weaker, or what flaw it contains.

Every argument has premises (the evidence) and a conclusion (the claim). An assumption is an unstated premise the argument needs. If the assumption were false, the argument would fall apart. To find it, ask "what must be true for this conclusion to work?"

To weaken an argument, look for an option that gives another explanation for the evidence or breaks the link between evidence and claim. To strengthen it, look for an option that rules out other explanations or adds direct support.

Classic flaws: mistaking correlation for cause (two things happening together doesn't mean one causes the other), generalising from one example, and assuming popularity proves quality.
""",
        [
            "Separate the evidence from the claim.",
            "Assumption = what must be true for the claim to hold.",
            "Weaken with an alternative explanation; strengthen by ruling alternatives out.",
        ],
        [
            rule("Argument", "Premises → Conclusion"),
            rule("Assumption test", "If it were false, would the argument collapse?"),
            rule("Correlation ≠ causation", "A and B rising together may share a third cause"),
        ],
        [
            "The best weakener usually attacks the link between the evidence and the conclusion, not the evidence itself.",
            "Ignore options that are true but irrelevant to the argument.",
        ],
        [
            ex("Statement: 'Join our coaching class to crack placement aptitude tests.' What does this assume?",
               ["The advert's claim only makes sense if coaching can make a difference.", "So it assumes coaching can improve aptitude test performance."],
               "Coaching can improve performance in aptitude tests."),
            ex("Argument: Umbrella sales rose after an advertising campaign, so the campaign worked. What would weaken this?",
               ["Look for another reason umbrella sales might rise.", "If the campaign ran during an unusually rainy month, the rain could explain the sales."],
               "The campaign coincided with an unusually rainy month."),
        ],
        [
            q("Argument: Students who sit in the front row score higher marks, so sitting in the front improves marks. Which statement most weakens this argument?",
              ["Front-row seats are closer to the board.", "Many classrooms have a front row.",
               "Students who already study more tend to choose front-row seats.", "Marks are given by teachers."],
              "C", "If hard-working students choose the front row, their study habits (not the seat) could explain the higher marks."),
            q("Statement: 'Use our app daily to improve your vocabulary.' Which is an assumption behind this statement?",
              ["Everyone owns a smartphone.", "Vocabulary can be improved through regular practice.", "Books are useless.", "The app is free."],
              "B", "The advice only makes sense if regular practice can improve vocabulary."),
            q("Argument: Our town's air pollution fell after new factory rules began, so the rules reduced pollution. Which statement most strengthens this argument?",
              ["The town has many trees.", "Factories are noisy.", "The rules were announced on TV.",
               "Pollution did not fall in nearby towns without such rules."],
              "D", "If similar towns without the rules saw no fall, the rules are the likely cause."),
            q("Which of these is a fact rather than an opinion?",
              ["Water boils at 100 °C at sea level.", "Summer is the best season.", "Maths is more interesting than history.", "Cricket is boring."],
              "A", "Only the first can be checked and proved; the others are personal preferences.", "easy"),
        ],
        [
            q("Argument: Ice-cream sales and drowning cases both rise in summer, so eating ice cream causes drowning. What is the flaw?",
              ["Ice cream is unhealthy.", "It mistakes correlation for cause; hot weather drives both.",
               "Drowning happens only in summer.", "The data comes from one city."],
              "B", "Both rise because of hot weather. Happening together doesn't mean one causes the other."),
            q("Notice: 'Please switch off the lights when you leave the room.' Which is an assumption behind it?",
              ["The room has no windows.", "Electricity is free.", "Leaving lights on unnecessarily wastes electricity.", "Everyone leaves the room."],
              "C", "The request only makes sense if lights left on waste electricity.", "easy"),
            q("Argument: Candidates who practise mock tests clear the placement aptitude round more often, so mock tests improve performance. Which most strengthens this?",
              ["Mock tests are available online.", "Some students dislike mock tests.", "The aptitude round has 30 questions.",
               "Among students of similar ability, those who practised mock tests scored higher."],
              "D", "Comparing students of similar ability rules out the idea that only stronger students take mock tests."),
            q("Argument: 'This medicine works, because my cold went away three days after I took it.' Which most weakens this?",
              ["Most colds go away on their own within a few days.", "The medicine is expensive.", "The medicine tastes bitter.", "Many people take medicines."],
              "A", "If colds clear up on their own in a few days, recovery says nothing about the medicine."),
            q("Every member of the coding club has passed the Python course. Arjun has not passed the Python course. What can be inferred?",
              ["Arjun will join the club soon.", "The Python course is difficult.", "Arjun is not a member of the coding club.", "Arjun knows Java."],
              "C", "Every member has passed; Arjun hasn't, so he can't be a member."),
            q("A company says, 'Our product is the best because it is the most popular.' What reasoning error is this?",
              ["Using too much data.", "Assuming popularity proves quality.", "Comparing two products.", "Giving a definition."],
              "B", "Something can be popular for reasons other than quality (price, advertising). Popularity alone doesn't prove it's best."),
        ],
    ),
]
