"""Quantitative Aptitude: original lessons and questions.

Numeric questions carry a `check` function that recomputes the answer; tests/test_content.py
verifies it against the correct option, so the answer keys can't silently drift.
"""

from math import comb, factorial, sqrt

from app.seed.builders import ex, q, rule, table, topic

SALES_TABLE = table(
    ["Year", "Laptops", "Phones"],
    [["2020", 40, 80], ["2021", 45, 90], ["2022", 50, 100], ["2023", 60, 110], ["2024", 75, 120]],
    "Units sold by a company (in thousands)",
)

MARKS_TABLE = table(
    ["Student", "Maths", "Science", "English"],
    [["Asha", 85, 78, 92], ["Bilal", 72, 80, 68], ["Chetna", 90, 88, 75], ["Dinesh", 64, 70, 80], ["Esha", 78, 82, 85]],
    "Marks of five students (each out of 100)",
)

QUANT_TOPICS = [
    topic(
        "percentages",
        "Percentages",
        "Percent of a number, percentage change and successive changes.",
        """
"Per cent" means "per hundred". 15% is simply 15/100, so 15% of 240 is 240 × 15/100 = 36. Almost every percentage question is a variation of this one idea.

Percentage change compares a change with the original value: (new − old) / old × 100. Always divide by the old value. That's why a rise from 40 to 50 is 25%, but a fall from 50 to 40 is only 20%.

When one change follows another, don't add the percentages. Multiply the factors instead, or use the shortcut a + b + ab/100. A 20% rise followed by a 20% fall gives 20 − 20 + (20 × −20)/100 = −4, a net 4% fall.

Learn the common fraction equivalents (1/8 = 12.5%, 1/6 ≈ 16.67%, 1/3 ≈ 33.33%). They turn many questions into one-line mental maths.
""",
        [
            "x% of y = x × y / 100.",
            "Percentage change is always measured against the original value.",
            "Successive changes multiply; they don't add.",
        ],
        [
            rule("Percentage change", "(new − old) / old × 100"),
            rule("Successive changes a% and b%", "a + b + ab/100", "use negative values for decreases"),
            rule("A is r% more than B", "B is r / (100 + r) × 100 % less than A"),
            rule("Price up r%, keep spending same", "cut consumption by r / (100 + r) × 100 %"),
        ],
        [
            "Increase by 20% → multiply by 1.2. Decrease by 15% → multiply by 0.85.",
            "Fraction equivalents: 1/4 = 25%, 1/5 = 20%, 1/8 = 12.5%, 1/12 ≈ 8.33%.",
        ],
        [
            ex("A price rises by 20% and then falls by 20%. What is the net change?",
               ["Use a + b + ab/100 with a = 20, b = −20.", "20 − 20 + (20 × −20)/100 = −4."], "A 4% decrease."),
            ex("A's salary is 25% more than B's. By what percent is B's salary less than A's?",
               ["Let B = 100, so A = 125.", "B is 25 less than A, out of A's 125.", "25/125 × 100 = 20%."], "20% less."),
        ],
        [
            q("What is 15% of 240?", ["32", "36", "38", "40"], "B", "240 × 15/100 = 36.", "easy", check=lambda: 240 * 15 / 100),
            q("A number increased by 20% gives 360. What is the number?", ["288", "320", "300", "340"], "C",
              "1.2 × number = 360, so number = 360 / 1.2 = 300.", "easy", check=lambda: 360 / 1.2),
            q("The price of sugar rises from ₹40 to ₹50 per kg. What is the percentage increase?", ["25%", "20%", "30%", "10%"], "A",
              "(50 − 40)/40 × 100 = 25%.", "easy", check=lambda: (50 - 40) / 40 * 100),
            q("A student needs 40% to pass. He scores 180 marks and fails by 20 marks. What are the maximum marks?",
              ["450", "550", "600", "500"], "D", "The pass mark is 180 + 20 = 200, which is 40% of the total. Total = 200 / 0.4 = 500.",
              check=lambda: 200 / 0.4),
        ],
        [
            q("If 35% of a number is 140, what is the number?", ["380", "400", "420", "490"], "B",
              "Number = 140 / 0.35 = 400.", "easy", check=lambda: 140 / 0.35),
            q("A town of 20,000 people grows by 10% every year. What will its population be after 2 years?",
              ["24,000", "22,000", "24,200", "24,400"], "C", "20,000 × 1.1 × 1.1 = 24,200. Growth compounds on the new total each year.",
              check=lambda: 20000 * 1.1 ** 2),
            q("A's income is 20% less than B's. By what percent is B's income more than A's?", ["25%", "20%", "30%", "15%"], "A",
              "Let B = 100, A = 80. B is 20 more than A: 20/80 × 100 = 25%.", check=lambda: 20 / 80 * 100),
            q("A shopkeeper raises a price by 10% and then gives a 10% discount. What is the net change?",
              ["No change", "1% increase", "2% decrease", "1% decrease"], "D",
              "10 − 10 + (10 × −10)/100 = −1, a 1% decrease.", check=lambda: abs(10 - 10 + (10 * -10) / 100)),
            q("In an election between two candidates, the winner gets 60% of the votes and wins by 1,200 votes. How many votes were cast?",
              ["5,000", "6,000", "7,200", "4,800"], "B", "The margin is 60% − 40% = 20% of the votes. 20% = 1,200, so 100% = 6,000.",
              check=lambda: 1200 / 0.2),
            q("Petrol prices rise by 25%. By what percent must a driver cut consumption to keep spending the same?",
              ["25%", "15%", "20%", "30%"], "C", "Cut = 25/(100 + 25) × 100 = 20%.", "hard", check=lambda: 25 / 125 * 100),
        ],
    ),
    topic(
        "profit-and-loss",
        "Profit and Loss",
        "Cost price, selling price, profit %, discounts and marked price.",
        """
Every profit and loss question involves a few fixed terms. Cost price (CP) is what the seller paid. Selling price (SP) is what the buyer pays. If SP > CP there is a profit; if SP < CP, a loss.

Profit and loss percentages are always calculated on the cost price: Profit % = (SP − CP)/CP × 100. To go the other way, SP = CP × (100 + profit%)/100.

Shops often show a marked price (MP) and then offer a discount. Discount is always calculated on the marked price: SP = MP × (100 − discount%)/100. So a question can involve three prices: CP, MP and SP. Write all three down before calculating.

Two successive discounts combine like successive percentage changes: 20% then 10% is not 30%, it's 1 − 0.8 × 0.9 = 28%.
""",
        [
            "Profit % and loss % are on cost price.",
            "Discount % is on marked price.",
            "Write CP, MP and SP down separately.",
        ],
        [
            rule("Profit %", "(SP − CP) / CP × 100"),
            rule("Selling price", "SP = CP × (100 + P%) / 100"),
            rule("After discount", "SP = MP × (100 − D%) / 100"),
            rule("Same SP, x% gain and x% loss", "overall loss = x² / 100 %"),
            rule("False weight", "gain % = (true − false) / false × 100"),
        ],
        [
            "If CP of a items = SP of b items, profit % = (a − b)/b × 100.",
            "Mark-up m% then discount d% gives a net factor of (1 + m/100)(1 − d/100).",
        ],
        [
            ex("An item bought for ₹500 is sold for ₹600. What is the profit percentage?",
               ["Profit = 600 − 500 = ₹100.", "Profit % = 100/500 × 100 = 20%."], "20%"),
            ex("An item is marked at ₹1,200 and sold at a 15% discount, still making a 2% profit. What is its cost price?",
               ["SP = 1,200 × 0.85 = ₹1,020.", "SP = CP × 1.02, so CP = 1,020 / 1.02 = ₹1,000."], "₹1,000"),
        ],
        [
            q("A bag bought for ₹800 is sold for ₹920. What is the profit percentage?", ["12%", "15%", "18%", "20%"], "B",
              "(920 − 800)/800 × 100 = 15%.", "easy", check=lambda: (920 - 800) / 800 * 100),
            q("An item costing ₹450 is sold at a 10% loss. What is the selling price?", ["₹395", "₹410", "₹405", "₹415"], "C",
              "450 × 0.9 = ₹405.", "easy", check=lambda: 450 * 0.9),
            q("The marked price of a shirt is ₹2,000 and the discount is 20%. What is the selling price?",
              ["₹1,600", "₹1,800", "₹1,500", "₹1,700"], "A", "2,000 × 0.8 = ₹1,600.", "easy", check=lambda: 2000 * 0.8),
            q("Selling an article at ₹1,320 gives a 10% profit. What is its cost price?", ["₹1,188", "₹1,210", "₹1,250", "₹1,200"], "D",
              "CP = 1,320 / 1.1 = ₹1,200.", check=lambda: 1320 / 1.1),
        ],
        [
            q("A trader marks goods 40% above cost and gives a 25% discount. What is his profit percentage?", ["5%", "10%", "15%", "7.5%"], "A",
              "1.4 × 0.75 = 1.05, so the profit is 5%.", check=lambda: (1.4 * 0.75 - 1) * 100),
            q("By selling 12 pens for ₹100 a shopkeeper loses 20%. How many pens should he sell for ₹100 to gain 20%?",
              ["9", "8", "10", "6"], "B",
              "₹100 is 80% of the cost of 12 pens, so 12 pens cost ₹125. To gain 20%, 12 pens must sell for ₹150. For ₹100: 12 × 100/150 = 8 pens.",
              "hard", check=lambda: 12 * 100 / (100 / 0.8 * 1.2)),
            q("Successive discounts of 20% and 10% are equal to a single discount of:", ["30%", "25%", "28%", "32%"], "C",
              "1 − 0.8 × 0.9 = 0.28, so 28%.", check=lambda: (1 - 0.8 * 0.9) * 100),
            q("A man sells two phones for ₹9,900 each, gaining 10% on one and losing 10% on the other. What is the overall result?",
              ["No profit, no loss", "1% gain", "2% loss", "1% loss"], "D",
              "Cost prices: 9,900/1.1 = 9,000 and 9,900/0.9 = 11,000. Total CP ₹20,000, total SP ₹19,800, so a ₹200 (1%) loss.",
              "hard", check=lambda: (20000 - 19800) / 20000 * 100),
            q("A shopkeeper sells at cost price but uses a 900 g weight instead of 1 kg. What is his profit percentage?",
              ["10%", "11.11%", "9.09%", "12.5%"], "B", "He gains 100 g on every 900 g: 100/900 × 100 = 11.11%.",
              check=lambda: round(100 / 900 * 100, 2)),
            q("The cost price of 20 items equals the selling price of 16 items. What is the profit percentage?",
              ["25%", "20%", "16%", "30%"], "A", "20 CP = 16 SP, so SP/CP = 1.25: a 25% profit.", check=lambda: (20 - 16) / 16 * 100),
        ],
    ),
    topic(
        "ratio-and-proportion",
        "Ratios and Proportions",
        "Compare quantities, share amounts and combine ratios.",
        """
A ratio compares two quantities of the same kind. 3 : 5 means "for every 3 of the first there are 5 of the second". Ratios behave like fractions, so 6 : 10 simplifies to 3 : 5.

To share an amount in a ratio, add the parts and take each person's share of the total. Sharing ₹1,200 in the ratio 3 : 5 gives 3/8 × 1,200 = ₹450 and 5/8 × 1,200 = ₹750.

A proportion says two ratios are equal: a : b = c : d, which means ad = bc. This lets you find a missing term, called the fourth proportional.

When ratios share a middle term (A : B and B : C), make the B values equal before joining them. With A : B = 2 : 3 and B : C = 4 : 5, scale to 8 : 12 and 12 : 15, giving A : B : C = 8 : 12 : 15.
""",
        [
            "Share = part / total parts × amount.",
            "In a proportion a : b = c : d, ad = bc.",
            "Match the common term before combining ratios.",
        ],
        [
            rule("Share in ratio a : b", "first = a/(a + b) × total"),
            rule("Fourth proportional of a, b, c", "x = b × c / a"),
            rule("Mean proportional of a, b", "√(a × b)"),
            rule("Combine A:B and B:C", "make B equal, then read A : B : C"),
        ],
        [
            "Write a ratio as multiples: 3 : 5 means 3x and 5x. Then form an equation.",
            "Adding the same number to both terms changes a ratio; multiplying both doesn't.",
        ],
        [
            ex("Divide ₹1,200 between A and B in the ratio 3 : 5.",
               ["Total parts = 3 + 5 = 8.", "A = 3/8 × 1,200 = ₹450; B = 5/8 × 1,200 = ₹750."], "A gets ₹450, B gets ₹750."),
            ex("If A : B = 2 : 3 and B : C = 4 : 5, find A : B : C.",
               ["B is 3 in the first ratio and 4 in the second; make it 12 in both.", "A : B = 8 : 12 and B : C = 12 : 15."],
               "8 : 12 : 15"),
        ],
        [
            q("Divide ₹840 between A and B in the ratio 3 : 4. What is A's share?", ["₹480", "₹360", "₹320", "₹420"], "B",
              "A = 3/7 × 840 = ₹360.", "easy", check=lambda: 840 * 3 / 7),
            q("Find the fourth proportional to 4, 6 and 10.", ["12", "18", "15", "20"], "C", "4 : 6 = 10 : x, so x = 6 × 10 / 4 = 15.",
              "easy", check=lambda: 6 * 10 / 4),
            q("Find the mean proportional between 9 and 16.", ["12", "12.5", "13", "25"], "A", "√(9 × 16) = √144 = 12.",
              check=lambda: sqrt(9 * 16)),
            q("If A : B = 2 : 3 and B : C = 4 : 5, what is A : C?", ["2 : 5", "4 : 5", "6 : 15", "8 : 15"], "D",
              "Make B equal: A : B = 8 : 12, B : C = 12 : 15. So A : C = 8 : 15."),
        ],
        [
            q("The ratio of boys to girls in a class is 7 : 5. There are 84 boys. How many girls are there?", ["55", "60", "65", "70"], "B",
              "7 parts = 84, so 1 part = 12. Girls = 5 × 12 = 60.", "easy", check=lambda: 84 * 5 / 7),
            q("Two numbers are in the ratio 3 : 5. If 9 is subtracted from each, the ratio becomes 12 : 23. What is the smaller number?",
              ["27", "55", "33", "36"], "C",
              "(3x − 9)/(5x − 9) = 12/23 → 69x − 207 = 60x − 108 → x = 11. The smaller number is 33.", "hard",
              check=lambda: 3 * ((23 * 9 - 12 * 9) / (23 * 3 - 12 * 5))),
            q("₹1,800 is divided among A, B and C in the ratio 2 : 3 : 4. What is C's share?", ["₹800", "₹600", "₹400", "₹900"], "A",
              "C = 4/9 × 1,800 = ₹800.", check=lambda: 1800 * 4 / 9),
            q("The salaries of A and B are in the ratio 4 : 5. Each gets a ₹2,000 raise and the ratio becomes 6 : 7. What was A's original salary?",
              ["₹5,000", "₹6,000", "₹3,000", "₹4,000"], "D",
              "(4x + 2000)/(5x + 2000) = 6/7 → 28x + 14,000 = 30x + 12,000 → x = 1,000. A = ₹4,000.", "hard",
              check=lambda: 4 * ((7 * 2000 - 6 * 2000) / (6 * 5 - 7 * 4))),
            q("If x : y = 3 : 4, find (2x + 3y) : (3x + 2y).", ["17 : 18", "18 : 17", "9 : 8", "6 : 7"], "B",
              "Put x = 3, y = 4: (6 + 12) : (9 + 8) = 18 : 17."),
            q("A bag has ₹1, 50 paise and 25 paise coins in the ratio 1 : 2 : 4, worth ₹60 in all. How many 25 paise coins are there?",
              ["60", "40", "80", "100"], "C",
              "Value: x × 1 + 2x × 0.5 + 4x × 0.25 = 3x = 60, so x = 20. 25 paise coins = 4x = 80.", "hard",
              check=lambda: 4 * (60 / (1 + 2 * 0.5 + 4 * 0.25))),
        ],
    ),
    topic(
        "averages",
        "Averages",
        "Find averages and how they change when values are added or removed.",
        """
The average (arithmetic mean) is the total divided by the number of items: average = sum / count. Most average questions are really about the sum, so the most useful move is to convert averages back into totals.

For example, if 30 students average 15 years, their ages add up to 30 × 15 = 450. If a teacher joins and the average becomes 16, the new total is 31 × 16 = 496, so the teacher is 496 − 450 = 46.

For consecutive numbers, the average is simply the middle number. For the first n natural numbers it's (n + 1)/2.

Average speed is a special case. It is total distance divided by total time, not the average of the speeds. For two equal distances at speeds x and y, it's 2xy/(x + y).
""",
        [
            "Average × count = sum. Work with sums.",
            "For consecutive numbers the average is the middle value.",
            "Average speed = total distance / total time.",
        ],
        [
            rule("Average", "sum / number of items"),
            rule("First n natural numbers", "(n + 1) / 2"),
            rule("Replacement", "new value = old value + (count × change in average)"),
            rule("Average speed, equal distances", "2xy / (x + y)"),
        ],
        [
            "If one value changes by d, the average changes by d / n.",
            "When an item is added and the average rises, the new item is above the old average by (new count × rise).",
        ],
        [
            ex("The average of 5 numbers is 20. After one number is removed, the average of the rest is 18. What number was removed?",
               ["Sum of 5 numbers = 5 × 20 = 100.", "Sum of the remaining 4 = 4 × 18 = 72.", "Removed number = 100 − 72 = 28."], "28"),
            ex("The average age of 30 students is 15. When the teacher's age is included, the average becomes 16. How old is the teacher?",
               ["Students' total = 30 × 15 = 450.", "Total with teacher = 31 × 16 = 496.", "Teacher = 496 − 450 = 46."], "46 years"),
        ],
        [
            q("What is the average of 12, 15, 18, 21 and 24?", ["16", "18", "20", "17"], "B", "Sum = 90, count = 5, average = 18.", "easy",
              check=lambda: (12 + 15 + 18 + 21 + 24) / 5),
            q("What is the average of the first 10 natural numbers?", ["5", "6", "5.5", "10"], "C", "(10 + 1)/2 = 5.5.", "easy",
              check=lambda: sum(range(1, 11)) / 10),
            q("The average weight of 8 people rises by 2.5 kg when a person weighing 65 kg is replaced by a new person. What does the new person weigh?",
              ["85 kg", "75 kg", "80 kg", "90 kg"], "A", "The total rises by 8 × 2.5 = 20 kg, so the new person weighs 65 + 20 = 85 kg.",
              check=lambda: 65 + 8 * 2.5),
            q("A batsman averages 40 after 10 innings. How many runs must he score in the 11th innings to raise his average to 42?",
              ["52", "60", "84", "62"], "D", "Needed total = 11 × 42 = 462. Current total = 400. He needs 62.", check=lambda: 11 * 42 - 10 * 40),
        ],
        [
            q("The average of 7 consecutive numbers is 20. What is the largest of them?", ["23", "21", "26", "24"], "A",
              "The middle (4th) number is 20, so the numbers run 17 to 23.", "easy", check=lambda: 20 + 3),
            q("The average of 50 numbers is 30. If the numbers 35 and 45 are removed, what is the new average (to 2 decimal places)?",
              ["29.50", "29.58", "30.00", "28.75"], "B", "New sum = 1,500 − 80 = 1,420. New average = 1,420 / 48 ≈ 29.58.",
              check=lambda: round((50 * 30 - 35 - 45) / 48, 2)),
            q("The average of A, B and C is 40, and the average of A and B is 35. What is C?", ["45", "40", "50", "55"], "C",
              "A + B + C = 120 and A + B = 70, so C = 50.", check=lambda: 3 * 40 - 2 * 35),
            q("A car goes from P to Q at 40 km/h and returns at 60 km/h. What is the average speed for the round trip?",
              ["50 km/h", "48 km/h", "45 km/h", "52 km/h"], "B", "2 × 40 × 60 / (40 + 60) = 48 km/h.", check=lambda: 2 * 40 * 60 / (40 + 60)),
            q("The average age of a family of 5 is 24 years. The youngest member is 4. What was the average age of the family when the youngest was born?",
              ["20", "24", "30", "25"], "D",
              "Current total = 120. Four years ago the other 4 members totalled 120 − 4 − (4 × 4) = 100, an average of 25.", "hard",
              check=lambda: (5 * 24 - 4 - 4 * 4) / 4),
            q("The average salary of 20 workers is ₹15,000. Including the manager, the average rises by ₹1,000. What is the manager's salary?",
              ["₹16,000", "₹36,000", "₹35,000", "₹31,000"], "B", "New total = 21 × 16,000 = 3,36,000. Old total = 3,00,000. Manager = ₹36,000.",
              check=lambda: 21 * 16000 - 20 * 15000),
        ],
    ),
    topic(
        "time-and-work",
        "Time and Work",
        "Work rates, people working together, and pipes and cisterns.",
        """
Think of work as a rate. If A finishes a job in 10 days, A does 1/10 of the job each day. Rates add when people work together: A (1/10) and B (1/15) together do 1/10 + 1/15 = 1/6 of the job per day, so they finish in 6 days.

A neat shortcut for two workers is ab/(a + b) days. For three or more, add the fractions.

When the number of people, hours or days changes but the job stays the same, total effort stays constant: M₁ × D₁ × H₁ = M₂ × D₂ × H₂. If the amount of work changes too, divide each side by the work.

Pipes and cisterns are the same idea: a filling pipe adds its rate and a draining pipe subtracts it. A tank filled by a 6-hour pipe and drained by a 12-hour pipe fills at 1/6 − 1/12 = 1/12 per hour.
""",
        [
            "Rate = 1 / time. Rates of people working together add.",
            "Total effort (men × days × hours) stays constant for the same job.",
            "Draining pipes have negative rates.",
        ],
        [
            rule("Two workers together", "ab / (a + b) days"),
            rule("Combined rate", "1/a + 1/b + 1/c …"),
            rule("Constant work", "M₁ D₁ H₁ = M₂ D₂ H₂"),
            rule("Pair sums (A+B, B+C, C+A)", "A + B + C = half the sum of the three pair rates"),
        ],
        [
            "If A is k times as efficient as B, A takes 1/k of B's time.",
            "Using LCM of the days as 'total units of work' avoids fractions.",
        ],
        [
            ex("A can finish a job in 10 days and B in 15 days. How long will they take together?",
               ["A's rate = 1/10, B's rate = 1/15.", "Together = 1/10 + 1/15 = 5/30 = 1/6 per day.", "So they take 6 days."], "6 days"),
            ex("12 men can do a job in 18 days. How many days will 18 men take?",
               ["Total effort = 12 × 18 = 216 man-days.", "18 men need 216 / 18 = 12 days."], "12 days"),
        ],
        [
            q("A can do a job in 12 days and B in 24 days. How long will they take together?", ["6 days", "8 days", "9 days", "10 days"], "B",
              "1/12 + 1/24 = 3/24 = 1/8 per day, so 8 days.", "easy", check=lambda: 12 * 24 / (12 + 24)),
            q("15 men can build a wall in 20 days. How many days will 25 men take?", ["15", "10", "12", "16"], "C",
              "15 × 20 = 300 man-days; 300 / 25 = 12 days.", "easy", check=lambda: 15 * 20 / 25),
            q("Pipe A fills a tank in 6 hours and pipe B empties it in 12 hours. With both open, how long will the tank take to fill?",
              ["12 hours", "4 hours", "8 hours", "18 hours"], "A", "1/6 − 1/12 = 1/12 per hour, so 12 hours.", check=lambda: 1 / (1 / 6 - 1 / 12)),
            q("A and B together finish a job in 10 days. A alone takes 15 days. How long would B take alone?",
              ["20 days", "25 days", "24 days", "30 days"], "D", "B's rate = 1/10 − 1/15 = 1/30, so 30 days.", check=lambda: 1 / (1 / 10 - 1 / 15)),
        ],
        [
            q("A, B and C can do a job in 10, 12 and 15 days respectively. How long will they take working together?",
              ["5 days", "4 days", "6 days", "3 days"], "B", "1/10 + 1/12 + 1/15 = (6 + 5 + 4)/60 = 1/4, so 4 days.",
              check=lambda: 1 / (1 / 10 + 1 / 12 + 1 / 15)),
            q("A can do a job in 20 days. He works for 5 days, then B finishes the rest in 9 days. How long would B take alone?",
              ["15 days", "18 days", "12 days", "10 days"], "C", "A did 5/20 = 1/4. B did the remaining 3/4 in 9 days, so B alone takes 12 days.",
              check=lambda: 9 / (1 - 5 / 20)),
            q("A is twice as efficient as B. Together they finish a job in 14 days. How long would A take alone?",
              ["21 days", "28 days", "42 days", "18 days"], "A", "Rates 2x + x = 1/14, so x = 1/42 and A's rate is 1/21: 21 days.",
              check=lambda: 1 / (2 * (1 / 14) / 3)),
            q("8 men working 6 hours a day finish a job in 15 days. How many days will 12 men working 5 hours a day take?",
              ["10", "15", "14", "12"], "D", "8 × 6 × 15 = 720 man-hours. 12 × 5 = 60 man-hours a day, so 12 days.",
              check=lambda: 8 * 6 * 15 / (12 * 5)),
            q("Two pipes fill a tank in 20 and 30 minutes. A drain empties it in 60 minutes. With all three open, how long does the tank take to fill?",
              ["12 minutes", "15 minutes", "18 minutes", "20 minutes"], "B", "1/20 + 1/30 − 1/60 = (3 + 2 − 1)/60 = 1/15, so 15 minutes.",
              check=lambda: 1 / (1 / 20 + 1 / 30 - 1 / 60)),
            q("A and B can do a job in 12 days, B and C in 15 days, and C and A in 20 days. How long will A, B and C take together?",
              ["8 days", "12 days", "10 days", "9 days"], "C",
              "Adding the pairs: 2(A + B + C) = 1/12 + 1/15 + 1/20 = 1/5. So A + B + C = 1/10: 10 days.", "hard",
              check=lambda: 2 / (1 / 12 + 1 / 15 + 1 / 20)),
        ],
    ),
    topic(
        "time-speed-distance",
        "Time, Speed and Distance",
        "Speed formulas, trains, relative speed and boats.",
        """
Everything here comes from one formula: distance = speed × time. Rearranged, speed = distance / time and time = distance / speed. Before calculating, make the units match. To convert km/h to m/s multiply by 5/18; to go back multiply by 18/5.

Relative speed handles two moving objects. Moving in the same direction, subtract their speeds; in opposite directions, add them. A chase or a meeting point becomes a single object moving at the relative speed.

Train questions add one twist: the train has length. To pass a pole or a person, a train covers its own length. To pass a platform or bridge, it covers its length plus the platform's. To pass another train, it covers both trains' lengths at the relative speed.

For boats, downstream speed = boat + stream and upstream speed = boat − stream. So the boat's speed is the average of the two, and the stream's speed is half their difference.
""",
        [
            "D = S × T. Match units first.",
            "Same direction: subtract speeds. Opposite: add.",
            "A train passing something covers its own length plus that thing's length.",
        ],
        [
            rule("Unit conversion", "km/h × 5/18 = m/s"),
            rule("Average speed (equal distances)", "2xy / (x + y)"),
            rule("Train crossing", "time = (train length + object length) / relative speed"),
            rule("Boats", "down = u + v, up = u − v; stream = (down − up)/2"),
        ],
        [
            "Useful conversions: 18 km/h = 5 m/s, 36 = 10, 54 = 15, 72 = 20, 90 = 25.",
            "If two times differ by t minutes at two speeds, set up d/s₁ − d/s₂ = t/60.",
        ],
        [
            ex("Convert 72 km/h into m/s.", ["Multiply by 5/18.", "72 × 5/18 = 20."], "20 m/s"),
            ex("A 200 m train travelling at 72 km/h crosses a 300 m platform. How long does it take?",
               ["Speed = 72 × 5/18 = 20 m/s.", "Distance = 200 + 300 = 500 m.", "Time = 500 / 20 = 25 s."], "25 seconds"),
        ],
        [
            q("A car covers 240 km in 4 hours. What is its speed?", ["50 km/h", "60 km/h", "55 km/h", "65 km/h"], "B", "240 / 4 = 60 km/h.",
              "easy", check=lambda: 240 / 4),
            q("Convert 54 km/h into metres per second.", ["12 m/s", "18 m/s", "15 m/s", "20 m/s"], "C", "54 × 5/18 = 15 m/s.", "easy",
              check=lambda: 54 * 5 / 18),
            q("A 150 m long train passes a pole in 10 seconds. What is its speed in km/h?", ["54 km/h", "45 km/h", "60 km/h", "50 km/h"], "A",
              "150 / 10 = 15 m/s = 15 × 18/5 = 54 km/h.", check=lambda: 150 / 10 * 18 / 5),
            q("A boat moves at 10 km/h in still water and the stream flows at 2 km/h. How long does it take to go 24 km downstream?",
              ["3 hours", "2.5 hours", "2.4 hours", "2 hours"], "D", "Downstream speed = 12 km/h, so 24 / 12 = 2 hours.",
              check=lambda: 24 / (10 + 2)),
        ],
        [
            q("Two trains, 120 m and 180 m long, run in opposite directions at 40 km/h and 50 km/h. How long do they take to cross each other?",
              ["10 s", "12 s", "15 s", "18 s"], "B", "Relative speed = 90 km/h = 25 m/s. Distance = 300 m. Time = 12 s.",
              check=lambda: (120 + 180) / ((40 + 50) * 5 / 18)),
            q("Walking at 5 km/h, a man reaches 15 minutes late. Walking at 6 km/h, he reaches 5 minutes early. How far does he walk?",
              ["12 km", "8 km", "10 km", "15 km"], "C", "d/5 − d/6 = 20/60, so d/30 = 1/3 and d = 10 km.", "hard",
              check=lambda: (20 / 60) / (1 / 5 - 1 / 6)),
            q("A 240 m train moving at 54 km/h crosses a bridge in 30 seconds. How long is the bridge?",
              ["210 m", "240 m", "180 m", "450 m"], "A", "15 m/s × 30 s = 450 m covered. Bridge = 450 − 240 = 210 m.",
              check=lambda: 54 * 5 / 18 * 30 - 240),
            q("A thief runs at 8 km/h. A police officer starts chasing 15 minutes later at 10 km/h. How long after starting does the officer catch the thief?",
              ["30 minutes", "45 minutes", "2 hours", "1 hour"], "D",
              "The thief's lead is 8 × 1/4 = 2 km. The gap closes at 10 − 8 = 2 km/h, so it takes 1 hour.", "hard",
              check=lambda: (8 * 0.25) / (10 - 8)),
            q("A boat goes 30 km downstream in 2 hours and 18 km upstream in 3 hours. What is the speed of the stream?",
              ["3 km/h", "4.5 km/h", "5 km/h", "6 km/h"], "B", "Downstream 15 km/h, upstream 6 km/h. Stream = (15 − 6)/2 = 4.5 km/h.",
              check=lambda: (30 / 2 - 18 / 3) / 2),
            q("A car covers the first half of a journey at 30 km/h and the second half at 60 km/h. What is its average speed?",
              ["45 km/h", "42 km/h", "40 km/h", "50 km/h"], "C", "2 × 30 × 60 / (30 + 60) = 40 km/h.", check=lambda: 2 * 30 * 60 / 90),
        ],
    ),
    topic(
        "simple-compound-interest",
        "Simple and Compound Interest",
        "Interest on loans and deposits, simple and compounded.",
        """
Simple interest (SI) is charged only on the original amount (the principal). It's the same every year: SI = P × R × T / 100, where R is the yearly rate in percent and T is the time in years.

Compound interest (CI) is charged on the principal plus all interest added so far, so it grows faster. The amount after T years is A = P × (1 + R/100)^T, and CI = A − P.

For the same principal, rate and one year, SI and CI are equal. After that they drift apart. For two years, the difference is P × (R/100)². That formula alone answers many questions.

If interest is compounded half-yearly, halve the rate and double the number of periods. Quarterly: rate ÷ 4, periods × 4.
""",
        [
            "SI grows by the same amount every year.",
            "CI grows on the growing total.",
            "Half-yearly: rate ÷ 2, time × 2.",
        ],
        [
            rule("Simple interest", "SI = P × R × T / 100"),
            rule("Compound amount", "A = P (1 + R/100)^T"),
            rule("CI − SI for 2 years", "P × (R/100)²"),
            rule("Sum doubles at SI in T years", "R = 100 / T"),
        ],
        [
            "At 10% CI, amounts grow as 1.1, 1.21, 1.331 times the principal.",
            "A sum that doubles in n years at CI becomes 4 times in 2n years.",
        ],
        [
            ex("Find the simple interest on ₹5,000 at 8% per annum for 3 years.", ["SI = 5,000 × 8 × 3 / 100 = 1,200."], "₹1,200"),
            ex("Find the compound interest on ₹10,000 at 10% per annum for 2 years.",
               ["A = 10,000 × 1.1² = 12,100.", "CI = 12,100 − 10,000 = 2,100."], "₹2,100"),
        ],
        [
            q("Find the simple interest on ₹4,000 at 5% per annum for 2 years.", ["₹400", "₹200", "₹500", "₹450"], "A",
              "4,000 × 5 × 2 / 100 = ₹400.", "easy", check=lambda: 4000 * 5 * 2 / 100),
            q("At what rate of simple interest will ₹2,000 become ₹2,600 in 5 years?", ["5%", "8%", "6%", "4%"], "C",
              "Interest = 600 = 2,000 × R × 5 / 100, so R = 6%.", check=lambda: 600 * 100 / (2000 * 5)),
            q("Find the compound interest on ₹5,000 at 10% per annum for 2 years.", ["₹1,000", "₹1,050", "₹1,100", "₹1,025"], "B",
              "5,000 × 1.21 − 5,000 = ₹1,050.", check=lambda: 5000 * 1.1 ** 2 - 5000),
            q("Find the difference between CI and SI on ₹8,000 at 5% per annum for 2 years.", ["₹40", "₹10", "₹25", "₹20"], "D",
              "8,000 × (5/100)² = ₹20.", check=lambda: 8000 * (5 / 100) ** 2),
        ],
        [
            q("A sum doubles in 8 years at simple interest. What is the rate?", ["10%", "12.5%", "8%", "15%"], "B",
              "Doubling means interest = principal, so R × 8 = 100 and R = 12.5%.", check=lambda: 100 / 8),
            q("What is the amount after 3 years on ₹10,000 at 10% compound interest?", ["₹13,000", "₹13,310", "₹13,100", "₹13,331"], "B",
              "10,000 × 1.1³ = ₹13,310.", check=lambda: 10000 * 1.1 ** 3),
            q("In how many years will ₹6,000 earn ₹1,800 simple interest at 6% per annum?", ["4", "6", "5", "3"], "C",
              "1,800 = 6,000 × 6 × T / 100, so T = 5.", "easy", check=lambda: 1800 * 100 / (6000 * 6)),
            q("Find the compound interest on ₹16,000 at 10% per annum for 1 year, compounded half-yearly.",
              ["₹1,640", "₹1,600", "₹1,680", "₹1,620"], "A",
              "5% per half-year for 2 periods: 16,000 × (1.05² − 1) = 16,000 × 0.1025 = ₹1,640.", "hard",
              check=lambda: 16000 * (1.05 ** 2 - 1)),
            q("A sum becomes ₹8,820 in 2 years at 5% compound interest. What is the principal?", ["₹8,400", "₹7,800", "₹8,200", "₹8,000"], "D",
              "P = 8,820 / 1.05² = 8,820 / 1.1025 = ₹8,000.", check=lambda: 8820 / 1.05 ** 2),
            q("The difference between CI and SI on a sum at 10% per annum for 2 years is ₹50. What is the sum?",
              ["₹4,000", "₹5,000", "₹6,000", "₹5,500"], "B", "P × (10/100)² = 50, so P × 0.01 = 50 and P = ₹5,000.", "hard",
              check=lambda: 50 / 0.01),
        ],
    ),
    topic(
        "number-system",
        "Number Systems",
        "Divisibility, HCF and LCM, remainders and unit digits.",
        """
Number system questions test how well you know integers. Four ideas cover most of them: divisibility rules, HCF and LCM, remainders, and unit digits.

Divisibility rules let you test numbers instantly. A number is divisible by 3 or 9 if its digit sum is; by 4 if its last two digits are; by 8 if its last three are; by 11 if the difference between the sums of alternate digits is 0 or a multiple of 11.

HCF is the largest number dividing all the given numbers; LCM is the smallest number all of them divide. For two numbers, HCF × LCM = product of the numbers. "Leaves remainder r when divided by a, b and c" questions usually mean LCM(a, b, c) + r.

Unit digits of powers repeat in cycles of at most 4. For 7: 7, 9, 3, 1, 7 … To find the unit digit of 7⁴⁵, divide 45 by 4: remainder 1, so it's the first in the cycle, 7.
""",
        [
            "Digit sum tests divisibility by 3 and 9.",
            "HCF × LCM = product (for two numbers).",
            "Unit digits cycle every 4 powers (or fewer).",
        ],
        [
            rule("HCF and LCM", "HCF × LCM = a × b"),
            rule("Sum of first n naturals", "n (n + 1) / 2"),
            rule("Unit digit cycles", "2: 2,4,8,6  3: 3,9,7,1  7: 7,9,3,1  8: 8,4,2,6"),
            rule("Multiples of k up to N", "floor(N / k)"),
        ],
        [
            "Numbers ending in 0, 1, 5 or 6 keep the same unit digit at every power.",
            "If the remainder of the power ÷ 4 is 0, use the 4th term of the cycle.",
        ],
        [
            ex("Find the HCF and LCM of 12 and 18.",
               ["12 = 2² × 3, 18 = 2 × 3².", "HCF = 2 × 3 = 6; LCM = 2² × 3² = 36.", "Check: 6 × 36 = 216 = 12 × 18."], "HCF 6, LCM 36"),
            ex("Find the unit digit of 7⁴⁵.", ["Unit digits of powers of 7 cycle 7, 9, 3, 1.", "45 ÷ 4 leaves remainder 1.", "So it's the first in the cycle."], "7"),
        ],
        [
            q("Find the LCM of 8, 12 and 18.", ["36", "48", "72", "144"], "C", "8 = 2³, 12 = 2² × 3, 18 = 2 × 3². LCM = 2³ × 3² = 72.",
              "easy", check=lambda: 72),
            q("Which of these numbers is divisible by 9?", ["4,321", "5,436", "7,125", "8,102"], "B",
              "Digit sums: 10, 18, 15, 11. Only 18 is divisible by 9, so 5,436.", "easy"),
            q("What is the sum of the first 50 natural numbers?", ["1,250", "1,275", "1,300", "2,550"], "B", "50 × 51 / 2 = 1,275.",
              check=lambda: sum(range(1, 51))),
            q("The HCF of two numbers is 6 and their LCM is 180. One number is 30. What is the other?", ["36", "30", "54", "60"], "A",
              "Other = 6 × 180 / 30 = 36.", check=lambda: 6 * 180 / 30),
        ],
        [
            q("What is the unit digit of 3⁶⁵?", ["9", "7", "1", "3"], "D", "Powers of 3 cycle 3, 9, 7, 1. 65 ÷ 4 leaves 1, so the unit digit is 3.",
              check=lambda: pow(3, 65, 10)),
            q("What is the smallest number that leaves remainder 3 when divided by 5, 6 and 8?", ["123", "243", "63", "120"], "A",
              "LCM(5, 6, 8) = 120, so 120 + 3 = 123.", check=lambda: 120 + 3),
            q("What is the remainder when 2¹⁰ is divided by 7?", ["1", "2", "3", "4"], "B", "2¹⁰ = 1,024 = 7 × 146 + 2.", check=lambda: 2 ** 10 % 7),
            q("How many numbers from 1 to 100 are divisible by 7?", ["13", "15", "14", "16"], "C", "floor(100 / 7) = 14.", "easy",
              check=lambda: 100 // 7),
            q("What is the largest 4-digit number divisible by 12?", ["9,999", "9,984", "9,990", "9,996"], "D",
              "9,999 ÷ 12 leaves remainder 3, so 9,999 − 3 = 9,996.", check=lambda: 9999 - 9999 % 12),
            q("The 6-digit number 5432x4 is divisible by 9. What is the smallest possible digit x?", ["3", "0", "6", "1"], "B",
              "Digit sum = 18 + x. For divisibility by 9, x = 0 or 9; the smallest is 0.", "hard",
              check=lambda: min(x for x in range(10) if (5 + 4 + 3 + 2 + x + 4) % 9 == 0)),
        ],
    ),
    topic(
        "probability",
        "Probability",
        "Chance of events with coins, dice, cards and balls.",
        """
Probability measures how likely something is, on a scale from 0 (impossible) to 1 (certain). When every outcome is equally likely, P(event) = favourable outcomes / total outcomes.

List the sample space carefully. One coin has 2 outcomes; two coins have 4 (HH, HT, TH, TT); a die has 6; two dice have 36; a deck has 52 cards in 4 suits of 13, with 12 face cards (J, Q, K in each suit).

"At least one" questions are easiest by subtracting: P(at least one head) = 1 − P(no heads). For independent events (one doesn't affect the other), P(A and B) = P(A) × P(B). For "A or B", add the probabilities and subtract the overlap so it isn't counted twice.

When drawing without replacement, the second draw has one fewer item in total, so multiply the changing fractions: (5/8) × (4/7).
""",
        [
            "P = favourable / total, for equally likely outcomes.",
            "At least one = 1 − none.",
            "Without replacement, update the totals after each draw.",
        ],
        [
            rule("Basic probability", "P(E) = favourable / total"),
            rule("Complement", "P(not E) = 1 − P(E)"),
            rule("Independent events", "P(A and B) = P(A) × P(B)"),
            rule("Either event", "P(A or B) = P(A) + P(B) − P(A and B)"),
        ],
        [
            "Two dice: there are 6 ways to make a sum of 7, the most of any sum.",
            "Choosing r items from n: use nCr for the count of outcomes.",
        ],
        [
            ex("Two coins are tossed. What is the probability of at least one head?",
               ["Outcomes: HH, HT, TH, TT, so 4 in total.", "Only TT has no head.", "P = 1 − 1/4 = 3/4."], "3/4"),
            ex("A card is drawn from a deck of 52. What is the probability it is a king or a heart?",
               ["Kings: 4. Hearts: 13. The king of hearts is counted twice.", "Favourable = 4 + 13 − 1 = 16.", "P = 16/52 = 4/13."], "4/13"),
        ],
        [
            q("A die is thrown. What is the probability of getting an even number?", ["1/3", "1/2", "2/3", "1/6"], "B",
              "Even outcomes: 2, 4, 6, which is 3 out of 6 = 1/2.", "easy", check=lambda: 3 / 6),
            q("A bag has 4 red and 6 blue balls. One ball is drawn. What is the probability it is red?", ["2/5", "3/5", "1/4", "2/3"], "A",
              "4 red out of 10 = 2/5.", "easy", check=lambda: 4 / 10),
            q("Two dice are thrown. What is the probability that the sum is 7?", ["1/12", "5/36", "1/6", "7/36"], "C",
              "(1,6), (2,5), (3,4), (4,3), (5,2), (6,1): 6 of 36 = 1/6.",
              check=lambda: sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 7) / 36),
            q("A card is drawn from a deck of 52. What is the probability it is a face card (J, Q or K)?", ["1/13", "4/13", "1/4", "3/13"], "D",
              "12 face cards out of 52 = 3/13.", check=lambda: 12 / 52),
        ],
        [
            q("Three coins are tossed. What is the probability of exactly two heads?", ["1/2", "3/8", "1/4", "5/8"], "B",
              "Of 8 outcomes, HHT, HTH and THH have exactly two heads: 3/8.", check=lambda: comb(3, 2) / 8),
            q("A bag has 5 white and 3 black balls. Two are drawn without replacement. What is the probability both are white?",
              ["25/64", "5/14", "5/8", "3/14"], "B", "(5/8) × (4/7) = 20/56 = 5/14.", "hard", check=lambda: (5 / 8) * (4 / 7)),
            q("For independent events A and B, P(A) = 0.6 and P(B) = 0.5. What is the probability that both happen?",
              ["0.3", "1.1", "0.5", "0.6"], "A", "0.6 × 0.5 = 0.3.", "easy", check=lambda: 0.6 * 0.5),
            q("Two dice are thrown. What is the probability of getting a double (both dice showing the same number)?",
              ["1/36", "1/12", "1/3", "1/6"], "D", "6 doubles out of 36 outcomes = 1/6.", check=lambda: 6 / 36),
            q("A number is chosen from 1 to 20. What is the probability it is a multiple of 3 or 5?", ["9/20", "2/5", "1/2", "7/20"], "A",
              "Multiples of 3: 6; of 5: 4; of both (15): 1. Favourable = 6 + 4 − 1 = 9, so 9/20.",
              check=lambda: sum(1 for n in range(1, 21) if n % 3 == 0 or n % 5 == 0) / 20),
            q("From 3 boys and 2 girls, 2 children are chosen at random. What is the probability of choosing one boy and one girl?",
              ["2/5", "3/10", "3/5", "1/2"], "C", "Ways = 3 × 2 = 6 out of 5C2 = 10, so 3/5.", "hard", check=lambda: 3 * 2 / comb(5, 2)),
        ],
    ),
    topic(
        "permutations-combinations",
        "Permutations and Combinations",
        "Count arrangements (order matters) and selections (order doesn't).",
        """
Permutations count arrangements, where order matters: ABC and CBA are different. Combinations count selections, where order doesn't: choosing {A, B, C} is one choice however you list it.

Ask one question before using a formula: "If I swap two chosen items, do I get something different?" If yes, it's a permutation (seating, passwords, rankings). If no, it's a combination (teams, committees, handshakes).

Arranging all n different items gives n! ways. If some items repeat, divide by the factorial of each repeat count: the letters of APPLE give 5!/2! = 60 arrangements. Around a circle, fix one person and arrange the rest: (n − 1)!.

When items must stay together, glue them into a single block, arrange the blocks, then multiply by the arrangements inside the block.
""",
        [
            "Order matters → permutation. Order doesn't → combination.",
            "Repeated items: divide by the factorial of each repeat.",
            "Items together: treat them as one block.",
        ],
        [
            rule("Factorial", "n! = n × (n − 1) × … × 1"),
            rule("Permutations", "nPr = n! / (n − r)!"),
            rule("Combinations", "nCr = n! / (r! (n − r)!)"),
            rule("With repeats", "n! / (p! q! …)"),
            rule("Circular arrangements", "(n − 1)!"),
        ],
        [
            "nCr = nC(n − r), so 10C8 = 10C2 = 45.",
            "Diagonals of an n-sided polygon: nC2 − n.",
        ],
        [
            ex("In how many ways can the letters of WORD be arranged?", ["4 different letters.", "4! = 4 × 3 × 2 × 1 = 24."], "24"),
            ex("In how many ways can 3 people be chosen from 7?", ["Order doesn't matter: use 7C3.", "7C3 = 7 × 6 × 5 / (3 × 2 × 1) = 35."], "35"),
        ],
        [
            q("In how many ways can 5 people stand in a line?", ["25", "60", "100", "120"], "D", "5! = 120.", "easy", check=lambda: factorial(5)),
            q("In how many ways can 2 members be chosen from 6?", ["12", "15", "30", "36"], "B", "6C2 = 15.", "easy", check=lambda: comb(6, 2)),
            q("In how many ways can the letters of APPLE be arranged?", ["60", "120", "24", "30"], "A", "5 letters with P twice: 5!/2! = 60.",
              check=lambda: factorial(5) // factorial(2)),
            q("How many 3-digit numbers can be formed from the digits 1–5 if digits may repeat?", ["60", "100", "125", "150"], "C",
              "5 choices for each of 3 places: 5³ = 125.", check=lambda: 5 ** 3),
        ],
        [
            q("In how many ways can the letters of BANANA be arranged?", ["720", "120", "360", "60"], "D",
              "6 letters with A three times and N twice: 6!/(3! × 2!) = 60.", check=lambda: factorial(6) // (factorial(3) * factorial(2))),
            q("A committee of 3 men and 2 women is chosen from 6 men and 4 women. In how many ways can this be done?",
              ["120", "200", "60", "240"], "A", "6C3 × 4C2 = 20 × 6 = 120.", check=lambda: comb(6, 3) * comb(4, 2)),
            q("In how many ways can 6 people sit around a round table?", ["720", "120", "360", "60"], "B", "(6 − 1)! = 120.",
              check=lambda: factorial(5)),
            q("How many diagonals does a hexagon have?", ["6", "12", "9", "15"], "C", "6C2 − 6 = 15 − 6 = 9.", check=lambda: comb(6, 2) - 6),
            q("In how many ways can the letters of LEADER be arranged?", ["720", "180", "240", "360"], "D",
              "6 letters with E twice: 6!/2! = 360.", check=lambda: factorial(6) // factorial(2)),
            q("In how many ways can the letters of MOTHER be arranged so that the vowels are always together?",
              ["120", "240", "720", "360"], "B", "Treat O and E as one block: 5 units → 5! = 120, times 2! inside the block = 240.", "hard",
              check=lambda: factorial(5) * factorial(2)),
        ],
    ),
    topic(
        "mixtures-alligations",
        "Mixtures and Alligations",
        "Mix two ingredients to a target price or strength.",
        """
Mixture questions combine two things (two grades of rice, two solutions, milk and water) and ask about the ratio or the result. The alligation rule is a shortcut for the most common case.

Alligation: to mix a cheaper item (price c) and a dearer item (price d) to get a mean price m, the quantities must be in the ratio (d − m) : (m − c), cheaper to dearer. Draw it as a cross: write c and d on top, m in the middle, and subtract diagonally.

For "add water / add milk" questions, the trick is that one ingredient stays fixed. If you add water, the amount of milk doesn't change, so work from the milk.

Repeated replacement (remove x litres, refill with water, repeat n times) leaves: original quantity × (1 − x/total)ⁿ of the original liquid.
""",
        [
            "Alligation ratio (cheaper : dearer) = (dearer − mean) : (mean − cheaper).",
            "When adding one ingredient, the other stays fixed.",
            "Repeated replacement shrinks by the same factor each time.",
        ],
        [
            rule("Alligation", "cheaper : dearer = (d − m) : (m − c)"),
            rule("Weighted mean", "(q₁ p₁ + q₂ p₂) / (q₁ + q₂)"),
            rule("Repeated replacement", "left = Q × (1 − x/Q)ⁿ"),
        ],
        [
            "Alligation works for prices, percentages, speeds or any averaged quantity.",
            "Check the answer: the mean must lie between the two values.",
        ],
        [
            ex("Rice at ₹40/kg is mixed with rice at ₹55/kg to get a mixture worth ₹45/kg. In what ratio are they mixed?",
               ["Cheaper : dearer = (55 − 45) : (45 − 40) = 10 : 5.", "Simplify to 2 : 1."], "2 : 1"),
            ex("A 40 L can of milk has 4 L removed and replaced with water, twice. How much milk is left?",
               ["Each step keeps (1 − 4/40) = 0.9 of the milk.", "40 × 0.9² = 32.4 L."], "32.4 litres"),
        ],
        [
            q("In what ratio must tea at ₹120/kg be mixed with tea at ₹150/kg to get a mixture worth ₹130/kg?",
              ["1 : 2", "2 : 1", "3 : 2", "1 : 1"], "B", "(150 − 130) : (130 − 120) = 20 : 10 = 2 : 1."),
            q("A 60 L mixture has milk and water in the ratio 2 : 1. How much water must be added to make the ratio 1 : 1?",
              ["10 L", "15 L", "30 L", "20 L"], "D", "Milk = 40 L, water = 20 L. For 1 : 1, water must be 40 L, so add 20 L.",
              check=lambda: 60 * 2 / 3 - 60 / 3),
            q("A 30 L solution is 20% sugar. How much water must be added to make it 15% sugar?", ["10 L", "5 L", "8 L", "12 L"], "A",
              "Sugar = 6 L, which must be 15% of the new total: 6 / 0.15 = 40 L. Add 10 L of water.", check=lambda: 30 * 0.2 / 0.15 - 30),
            q("Two alloys contain 40% and 70% gold. In what ratio should they be mixed to get 60% gold?", ["2 : 1", "3 : 4", "1 : 2", "1 : 1"], "C",
              "40% : 70% = (70 − 60) : (60 − 40) = 10 : 20 = 1 : 2."),
        ],
        [
            q("A container has 50 L of milk. 5 L is removed and replaced with water, and this is done once more. How much milk is left?",
              ["40 L", "40.5 L", "45 L", "41 L"], "B", "50 × (1 − 5/50)² = 50 × 0.81 = 40.5 L.", check=lambda: 50 * (1 - 5 / 50) ** 2),
            q("How many kg of rice at ₹30/kg must be mixed with 20 kg of rice at ₹45/kg to get a mixture worth ₹40/kg?",
              ["15 kg", "20 kg", "5 kg", "10 kg"], "D", "Cheaper : dearer = (45 − 40) : (40 − 30) = 1 : 2. With 20 kg of the dearer, use 10 kg.",
              check=lambda: 20 * (45 - 40) / (40 - 30)),
            q("A 40 L mixture of milk and water has 25% water. How much milk must be added so that water becomes 20%?",
              ["10 L", "8 L", "5 L", "12 L"], "A", "Water = 10 L, which must be 20% of the new total: 50 L. Add 10 L of milk.",
              check=lambda: 40 * 0.25 / 0.2 - 40),
            q("Pulses at ₹60/kg and ₹75/kg are mixed in the ratio 2 : 3. What is the price of the mixture per kg?",
              ["₹67.50", "₹70", "₹69", "₹68"], "C", "(2 × 60 + 3 × 75) / 5 = 345 / 5 = ₹69.", check=lambda: (2 * 60 + 3 * 75) / 5),
            q("80 L of a mixture has milk and water in the ratio 3 : 1. How much water must be added to make the ratio 3 : 2?",
              ["10 L", "20 L", "30 L", "40 L"], "B", "Milk = 60 L, water = 20 L. For 3 : 2, water must be 40 L, so add 20 L.",
              check=lambda: 80 * 3 / 4 * 2 / 3 - 80 / 4),
            q("From a vessel of 20 L of petrol, 4 L is drawn and replaced with kerosene. This is done three times. How much petrol is left?",
              ["10.24 L", "12.8 L", "8 L", "11.52 L"], "A", "20 × (1 − 4/20)³ = 20 × 0.512 = 10.24 L.", "hard",
              check=lambda: 20 * (1 - 4 / 20) ** 3),
        ],
    ),
    topic(
        "problems-on-ages",
        "Problems on Ages",
        "Set up equations from present, past and future ages.",
        """
Age problems are linear equations in disguise. The key fact: everyone ages at the same rate. If it's 5 years later for one person, it's 5 years later for everyone, so the difference between two people's ages never changes.

Let the unknown present age be x and write every other age in terms of x. "5 years ago" means x − 5; "in 12 years" means x + 12. Then turn the sentence into an equation and solve.

For ratio questions, write the present ages as 3k and 4k (for a 3 : 4 ratio), then add or subtract years from each.

Always check your answer against every condition in the question. A negative or impossible age means you mistranslated a clue.
""",
        [
            "Age differences never change.",
            "Write every age in terms of one unknown.",
            "For ratios, use multiples like 3k and 4k.",
        ],
        [
            rule("n years ago / later", "x − n  /  x + n"),
            rule("Ratio a : b", "ages ak and bk"),
        ],
        [
            "Average age questions: convert to total age first.",
            "Plug the options back in when an equation looks messy; it's often faster.",
        ],
        [
            ex("A father is 3 times as old as his son. In 12 years he will be twice as old. Find their present ages.",
               ["Son = x, father = 3x.", "3x + 12 = 2(x + 12) → 3x + 12 = 2x + 24 → x = 12.", "Father = 36."], "Son 12, father 36"),
            ex("The sum of A's and B's ages is 50. Five years ago their ages were in the ratio 3 : 2. Find their present ages.",
               ["Five years ago: 3k and 2k. Present: 3k + 5 and 2k + 5.", "5k + 10 = 50 → k = 8.", "A = 29, B = 21."], "A is 29, B is 21"),
        ],
        [
            q("Ravi is 6 years older than Sita, and the sum of their ages is 40. How old is Ravi?", ["17", "23", "20", "26"], "B",
              "x + (x + 6) = 40 → x = 17, so Ravi is 23.", "easy", check=lambda: (40 - 6) / 2 + 6),
            q("The ages of A and B are in the ratio 4 : 5 and their sum is 45. How old is A?", ["20", "25", "18", "24"], "A",
              "9 parts = 45, so A = 4 × 5 = 20.", "easy", check=lambda: 45 * 4 / 9),
            q("A mother is 30 years older than her daughter. In 5 years she will be 3 times as old as her daughter. How old is the daughter now?",
              ["8", "12", "10", "15"], "C", "D + 35 = 3(D + 5) → 2D = 20 → D = 10.", check=lambda: (35 - 15) / 2),
            q("Five years ago a man was 7 times as old as his son. Now he is 4 times as old. How old is the son?", ["8", "12", "15", "10"], "D",
              "4S − 5 = 7(S − 5) → 3S = 30 → S = 10.", check=lambda: 30 / 3),
        ],
        [
            q("The present ages of A and B are in the ratio 5 : 7. After 6 years the ratio will be 3 : 4. How old is A now?",
              ["25", "30", "35", "36"], "B", "(5x + 6)/(7x + 6) = 3/4 → 20x + 24 = 21x + 18 → x = 6, so A = 30.",
              check=lambda: 5 * (4 * 6 - 3 * 6) / (3 * 7 - 4 * 5)),
            q("Five children were born at intervals of 3 years and their ages add up to 50. How old is the youngest?", ["4", "5", "6", "3"], "A",
              "x + (x + 3) + (x + 6) + (x + 9) + (x + 12) = 5x + 30 = 50, so x = 4.", check=lambda: (50 - 30) / 5),
            q("A father is now twice as old as his son. Twenty years ago he was 12 times as old. How old is the father now?",
              ["40", "48", "44", "42"], "C", "2S − 20 = 12(S − 20) → 10S = 220 → S = 22, so the father is 44.", "hard",
              check=lambda: 2 * ((12 * 20 - 20) / (12 - 2))),
            q("A husband and wife had an average age of 23 when they married. Five years later, with a one-year-old child, what is the family's average age?",
              ["23", "21", "20", "19"], "D", "The couple now totals 46 + 10 = 56. With the child, 57 / 3 = 19.", "hard",
              check=lambda: (2 * 23 + 2 * 5 + 1) / 3),
            q("Ten years ago A was half B's age. Their present ages are in the ratio 3 : 4. What is the sum of their present ages?",
              ["35", "28", "42", "49"], "A", "3k − 10 = (4k − 10)/2 → 6k − 20 = 4k − 10 → k = 5. Sum = 7k = 35.",
              check=lambda: 7 * ((20 - 10) / (6 - 4))),
            q("Rohan's age in 15 years will be 5 times his age 5 years ago. How old is he now?", ["12", "10", "8", "15"], "B",
              "R + 15 = 5(R − 5) → 4R = 40 → R = 10.", check=lambda: (15 + 25) / 4),
        ],
    ),
    topic(
        "data-interpretation",
        "Data Interpretation",
        "Read tables and calculate totals, averages, ratios and changes.",
        """
Data interpretation (DI) gives you a table or chart and several questions about it. The maths is simple (sums, averages, percentages, ratios). The skill is reading the data accurately and quickly.

First read the title, the column headings and the units. "In thousands" or "out of 100" changes every answer. Then read the question and pick out exactly which cells it needs. Don't calculate anything it doesn't ask for.

Percentage change in DI is the same formula as always: (new − old) / old × 100. "Which year had the highest ratio" questions are faster if you compare fractions roughly before calculating precisely.

When options are far apart, approximate. When they're close, calculate carefully. Placement tests reward knowing which situation you're in.
""",
        [
            "Read the title, headings and units first.",
            "Pull out only the cells the question needs.",
            "Approximate when options are far apart.",
        ],
        [
            rule("Percentage change", "(new − old) / old × 100"),
            rule("Share of total", "part / total × 100"),
            rule("Average across years", "sum of values / number of years"),
        ],
        [
            "Compare ratios by cross-multiplying instead of dividing.",
            "Keep a running total when a question needs several sums from the same row.",
        ],
        [
            ex("A company sold 40 thousand laptops in 2020 and 60 thousand in 2023. What was the percentage increase?",
               ["Change = 60 − 40 = 20 thousand.", "Percentage increase = 20/40 × 100 = 50%."], "50%"),
            ex("Three students scored 70, 85 and 91 in Maths. What is their average score?",
               ["Sum = 70 + 85 + 91 = 246.", "Average = 246 / 3 = 82."], "82"),
        ],
        [
            q("Using the table, how many units (in thousands) were sold in total in 2022?", ["140", "150", "160", "155"], "B",
              "2022: 50 laptops + 100 phones = 150 thousand.", "easy", table=SALES_TABLE, check=lambda: 50 + 100),
            q("Using the table, what was the percentage increase in laptop sales from 2023 to 2024?", ["15%", "20%", "25%", "30%"], "C",
              "(75 − 60)/60 × 100 = 25%.", table=SALES_TABLE, check=lambda: (75 - 60) / 60 * 100),
            q("Using the table, what were the average yearly phone sales from 2020 to 2024 (in thousands)?", ["100", "95", "105", "110"], "A",
              "(80 + 90 + 100 + 110 + 120)/5 = 500/5 = 100.", table=SALES_TABLE, check=lambda: (80 + 90 + 100 + 110 + 120) / 5),
            q("Using the table, in which year was the ratio of laptops to phones sold the highest?", ["2021", "2022", "2023", "2024"], "D",
              "Ratios: 0.5, 0.5, 0.5, 0.55 and 0.625. The highest is 2024 (75/120).", table=SALES_TABLE),
        ],
        [
            q("Using the table, what are Chetna's total marks?", ["243", "253", "263", "250"], "B", "90 + 88 + 75 = 253.", "easy",
              table=MARKS_TABLE, check=lambda: 90 + 88 + 75),
            q("Using the table, what is the average Maths score of the five students?", ["77.8", "78.2", "76.4", "79.0"], "A",
              "(85 + 72 + 90 + 64 + 78)/5 = 389/5 = 77.8.", table=MARKS_TABLE, check=lambda: (85 + 72 + 90 + 64 + 78) / 5),
            q("Using the table, which student has the highest total marks?", ["Chetna", "Esha", "Asha", "Bilal"], "C",
              "Totals: Asha 255, Bilal 220, Chetna 253, Dinesh 214, Esha 245. Asha is highest.", table=MARKS_TABLE),
            q("Using the table, Dinesh's English marks are what percentage of his total marks (to one decimal place)?",
              ["33.3%", "35.5%", "40.2%", "37.4%"], "D", "Total = 64 + 70 + 80 = 214. 80/214 × 100 ≈ 37.4%.", "hard",
              table=MARKS_TABLE, check=lambda: round(80 / 214 * 100, 1)),
            q("Using the table, by how many marks does Esha's Science score exceed the average Science score?", ["2.4", "3.2", "1.6", "2.0"], "A",
              "Average Science = (78 + 80 + 88 + 70 + 82)/5 = 79.6. 82 − 79.6 = 2.4.", "hard", table=MARKS_TABLE,
              check=lambda: round(82 - (78 + 80 + 88 + 70 + 82) / 5, 1)),
            q("Using the table, what is the ratio of Bilal's Maths marks to Asha's English marks?", ["9 : 11", "18 : 23", "3 : 4", "23 : 18"], "B",
              "72 : 92 = 18 : 23.", table=MARKS_TABLE),
        ],
    ),
    topic(
        "simplification",
        "Simplification",
        "BODMAS, fractions, decimals, squares and quick approximation.",
        """
Simplification questions are pure calculation, and the clock is the real opponent. Two habits make you fast: following the order of operations every time, and spotting algebraic shortcuts.

BODMAS gives the order: Brackets, Orders (powers and roots), Division and Multiplication (left to right), then Addition and Subtraction (left to right). 24 + 16 ÷ 4 × 3 − 5 means 16 ÷ 4 = 4, then 4 × 3 = 12, then 24 + 12 − 5 = 31.

Algebraic identities turn ugly arithmetic into one step. 102 × 98 = (100 + 2)(100 − 2) = 10,000 − 4 = 9,996. And 1.2² + 2 × 1.2 × 0.8 + 0.8² is just (1.2 + 0.8)² = 4.

For "approximately equal to" questions, round each number to something friendly (49.97% ≈ 50%, 601.02 ≈ 600) and compute quickly. The options are usually far enough apart.
""",
        [
            "Follow BODMAS strictly: ÷ and × left to right, then + and −.",
            "Look for (a + b)², (a − b)² and (a + b)(a − b) patterns.",
            "In approximation questions, round first, then calculate.",
        ],
        [
            rule("BODMAS", "Brackets → Orders → ÷ × → + −"),
            rule("Square of a sum", "(a + b)² = a² + 2ab + b²"),
            rule("Difference of squares", "(a + b)(a − b) = a² − b²"),
            rule("Squares near 100", "(100 − k)² = 10,000 − 200k + k²"),
        ],
        [
            "x% of y = y% of x, so 25% of 48 = 48% of 25 = 12.",
            "Memorise squares up to 30 and cubes up to 15.",
        ],
        [
            ex("Simplify 18 ÷ 3 × 2 + 4 − 6.", ["Left to right for ÷ and ×: 18 ÷ 3 = 6, then 6 × 2 = 12.", "12 + 4 − 6 = 10."], "10"),
            ex("Find 999 × 999.", ["999 = 1,000 − 1.", "(1,000 − 1)² = 1,000,000 − 2,000 + 1 = 998,001."], "998,001"),
        ],
        [
            q("24 + 16 ÷ 4 × 3 − 5 = ?", ["31", "25", "35", "15"], "A", "16 ÷ 4 = 4; 4 × 3 = 12; 24 + 12 − 5 = 31.", "easy",
              check=lambda: 24 + 16 / 4 * 3 - 5),
            q("(0.5 × 0.5 + 0.5) ÷ 0.5 = ?", ["1", "0.75", "1.5", "2"], "C", "(0.25 + 0.5) ÷ 0.5 = 0.75 ÷ 0.5 = 1.5.", check=lambda: (0.5 * 0.5 + 0.5) / 0.5),
            q("25% of 480 + 15% of 200 = ?", ["140", "150", "160", "130"], "B", "120 + 30 = 150.", "easy", check=lambda: 0.25 * 480 + 0.15 * 200),
            q("102 × 98 = ?", ["10,004", "9,904", "9,994", "9,996"], "D", "(100 + 2)(100 − 2) = 10,000 − 4 = 9,996.", check=lambda: 102 * 98),
        ],
        [
            q("√1764 = ?", ["38", "42", "44", "46"], "B", "42 × 42 = 1,764.", "easy", check=lambda: sqrt(1764)),
            q("3/4 of 2/5 of 1,200 = ?", ["300", "320", "360", "400"], "C", "2/5 × 1,200 = 480; 3/4 × 480 = 360.", check=lambda: 0.75 * 0.4 * 1200),
            q("(48 ÷ 6) × 4 + 3² − 7 = ?", ["34", "32", "30", "38"], "A", "8 × 4 = 32; 32 + 9 − 7 = 34.", check=lambda: (48 / 6) * 4 + 3 ** 2 - 7),
            q("1.2 × 1.2 + 2 × 1.2 × 0.8 + 0.8 × 0.8 = ?", ["3.6", "2", "4.4", "4"], "D", "This is (1.2 + 0.8)² = 2² = 4.", "hard",
              check=lambda: 1.2 * 1.2 + 2 * 1.2 * 0.8 + 0.8 * 0.8),
            q("49.97% of 601.02 is approximately:", ["250", "280", "300", "320"], "C", "≈ 50% of 600 = 300.",
              check=lambda: round(0.4997 * 601.02 / 10) * 10),
            q("1/2 + 1/3 + 1/6 = ?", ["1", "5/6", "2/3", "7/6"], "A", "3/6 + 2/6 + 1/6 = 6/6 = 1.", "easy", check=lambda: 1 / 2 + 1 / 3 + 1 / 6),
        ],
    ),
]
