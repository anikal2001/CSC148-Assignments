import course
import survey
import criterion
import grouper
import pytest
from typing import List, Set, FrozenSet


@pytest.fixture
def questions() -> List[survey.Question]:
    return [survey.MultipleChoiceQuestion(1, 'why?', ['a', 'b']),
            survey.NumericQuestion(2, 'what?', -2, 4),
            survey.YesNoQuestion(3, 'really?'),
            survey.CheckboxQuestion(4, 'how?', ['a', 'b', 'c'])]


@pytest.fixture
def students() -> List[course.Student]:
    return [course.Student(1, 'Zoro'),
            course.Student(2, 'Aaron'),
            course.Student(3, 'Gertrude'),
            course.Student(4, 'Yvette'),
            course.Student(6, 'Steph'),
            course.Student(7, 'Draymond'),
            course.Student(8, 'Andrew')]

@pytest.fixture
def students1() -> List[course.Student]:
    return [course.Student(1, 'Zoro'),
            course.Student(2, 'Aaron'),
            course.Student(3, 'Gertrude'),
            course.Student(4, 'Yvette'),
            course.Student(5, 'George'),
            course.Student(6, 'Steph'),
            course.Student(7, 'Draymond'),
            course.Student(8, 'Andrew')]


@pytest.fixture
def answers() -> List[List[survey.Answer]]:
    return [[survey.Answer('a'), survey.Answer('b'),
             survey.Answer('a'), survey.Answer('b')],
            [survey.Answer(0), survey.Answer(4),
             survey.Answer(-1), survey.Answer(1)],
            [survey.Answer(True), survey.Answer(False),
             survey.Answer(True), survey.Answer(True)],
            [survey.Answer(['a', 'b']), survey.Answer(['a', 'b']),
             survey.Answer(['a']), survey.Answer(['b'])]]


@pytest.fixture
def students_with_answers(students1, questions, answers) -> List[
    course.Student]:
    for i, student in enumerate(students1):
        for j, question in enumerate(questions):
            student.set_answer(question, answers[j][i])
    return students


@pytest.fixture
def course_with_students(empty_course, students) -> course.Course:
    empty_course.enroll_students(students)
    return empty_course


@pytest.fixture
def course_with_students_with_answers(empty_course,
                                      students_with_answers) -> course.Course:
    empty_course.enroll_students(students_with_answers)
    return empty_course


class TestStudent:
    def test_init(self) -> None:
        s = course.Student(1, 'Bob')
        s1 = course.Student(2, '')
        assert s.id == 1
        assert s.name == 'Bob'

    def test_str_method(self) -> None:
        s = course.Student(1, 'Bob')
        assert str(s) == 'Bob'

    def test_has_answer(self, questions):
        s = course.Student(1, 'Bob')
        s1 = course.Student(2, 'George')
        s2 = course.Student(3, 'Dylan')
        s.set_answer(questions[0], survey.Answer('a'))
        s1.set_answer(questions[0], survey.Answer('n'))
        assert s.has_answer(questions[0]) is True
        assert s1.has_answer(questions[0]) is False
        assert s2.has_answer(questions[0]) is False

    def test_set_answer(self, questions):
        s = course.Student(1, 'Bob')
        s.set_answer(questions[0], survey.Answer(2))
        assert s.get_answer(questions[0]).content == 2
        s.set_answer(questions[0], survey.Answer(4))
        assert s.get_answer(questions[0]).content == 4

    def test_get_answer(self, questions):
        s = course.Student(2, 'George')
        assert s.get_answer(questions[0]) is None
        s.set_answer(questions[0], survey.Answer('4'))
        assert s.get_answer(questions[0]).content == '4'


class TestCourse:
    def test_enroll_students(self):
        new_course = course.Course('CSC148')
        students = [course.Student(1, 'Zoro'),
                    course.Student(2, 'Aaron'),
                    course.Student(3, 'Gertrude'),
                    course.Student(4, 'Yvette'),
                    course.Student(4, 'George'),
                    course.Student(6, 'Steph'),
                    course.Student(7, 'Draymond'),
                    course.Student(8, 'Andrew')]
        new_course.enroll_students(students)
        assert len(new_course.students) == 0
        new_course = course.Course('CSC165')
        students = [course.Student(1, 'Zoro'),
                    course.Student(2, 'Aaron'),
                    course.Student(3, 'Gertrude')]
        new_course.enroll_students(students)
        new_course.enroll_students(students)
        assert len(new_course.students) == 3

    def test_all_answered(self, answers, questions):
        new_course = course.Course('CSC148')
        students = [course.Student(1, 'Zoro'),
                    course.Student(2, 'Aaron'),
                    course.Student(3, 'Gertrude'),
                    course.Student(4, 'Yvette'),
                    course.Student(6, 'Steph'),
                    course.Student(7, 'Draymond'),
                    course.Student(8, 'Andrew')]
        s = survey.Survey(questions)
        new_course.enroll_students(students)
        assert new_course.all_answered(s) == False

    def test_get_students(self):
        new_course = course.Course('CSC148')
        students = [course.Student(1, 'Zoro'),
                    course.Student(2, 'Aaron'),
                    course.Student(3, 'Gertrude'),
                    course.Student(4, 'Yvette'),
                    course.Student(6, 'Steph'),
                    course.Student(7, 'Draymond'),
                    course.Student(8, 'Andrew')]
        new_course.enroll_students(students)
        assert len(new_course.get_students()) == 7
        assert isinstance(new_course.get_students(), tuple)


class TestMCQuestion:
    def test_init(self, questions) -> None:
        assert questions[0].id == 1
        assert questions[0].text == 'why?'
        assert len(questions[0].options) == 2
        assert questions[0].options[0] == 'a'

    def test_str(self, questions) -> None:
        assert isinstance(str(questions[0]), str) == True
        assert 'why?' in str(questions[0]) and 'a' in str(questions[0])

    def test_validate_answer(self, questions, answers) -> None:
        ques = questions[0]
        assert ques.validate_answer(answers[0][0]) is True
        assert ques.validate_answer(answers[0][1]) is True

    def test_get_similarity(self, answers, questions) -> None:
        ques = questions[0]
        ans1 = survey.Answer(['a', 'b', 'c'])
        ans2 = survey.Answer(['a', 'b', 'c'])
        assert ques.get_similarity(ans1, ans2) == 1



class TestNumeric_Question:
    def test_init(self, questions) -> None:
        assert questions[1].id == 2
        assert questions[1].text == 'what?'
        assert questions[1].min == -2
        assert questions[1].max == 4

    def test_str(self, questions) -> None:
        assert 'what?' in str(questions[1])
        assert '-2' in str(questions[1])
        assert '4' in str(questions[1])

    def test_validate_answer(self, questions) -> None:
        a1 = survey.Answer(1)
        assert questions[1].validate_answer(a1) == True

    def test_get_similarity(self, questions) -> None:
        answer1 = survey.Answer(4)
        answer2 = survey.Answer(3)
        assert round(questions[1].get_similarity(answer1, answer2)) == 1


class TestYesNo_Question:
    def test_str(self, questions) -> None:
        assert 'really?' in str(questions[2])

    def test_validate_answer(self, questions) -> None:
        assert questions[2].validate_answer(survey.Answer(True)) is True

    def test_get_similarity(self, questions) -> None:
        answer1 = survey.Answer('Yes')
        answer2 = survey.Answer('No')
        assert questions[2].get_similarity(answer1, answer2) == 0.0


class TestCheckbox_Question:
    def test_str(self, questions) -> None:
        assert 'how?' in str(questions[3])

    def test_validate_answer(self, questions) -> None:
        assert questions[3].validate_answer(survey.Answer(['a'])) is True

    def test_get_similarity(self, questions) -> None:
        answer1 = survey.Answer(['a', 'b'])
        answer2 = survey.Answer(['a'])
        assert questions[3].get_similarity(answer1, answer2) == 0.5


class TestAnswer:
    def is_valid(self, question) -> None:
        pass


class TestGroup:
    def test_init(self, students) -> None:
        new_group = grouper.Group(students)
        assert id(new_group._members) != id(students)
        assert isinstance(new_group._members, list)
        assert len(new_group._members) == 7

    def test_len(self, students) -> None:
        new_group = grouper.Group(students)
        assert len(new_group) == 7

    def test_contains(self, students) -> None:
        new_group = grouper.Group(students)
        assert students[0] in new_group
        assert students[6] in new_group
        new_student = course.Student(12, 'George')
        assert new_student not in new_group

    def test_str(self, students) -> None:
        new_group = grouper.Group(students)
        assert students[0].name in str(new_group)
        assert students[6].name in str(new_group)

    def test_get_members(self, students) -> None:
        new_group = grouper.Group(students)
        group_members = new_group.get_members()
        assert id(group_members) != id(new_group._members)
        assert new_group.get_members() == group_members


class TestGrouping:
    def test_init(self):
        new_grouping = grouper.Grouping()
        assert len(new_grouping._groups) == 0

    def test_len(self, students):
        new_grouping = grouper.Grouping()
        group_list = grouper.slice_list(students, 2)
        for group in group_list:
            new_grouping.add_group(grouper.Group(group))
        assert len(new_grouping) == 4

    def test_str(self, students):
        new_grouping = grouper.Grouping()
        group_list = grouper.slice_list(students, 2)
        for group in group_list:
            new_grouping.add_group(grouper.Group(group))
        grouping_string = str(new_grouping)
        for group in new_grouping.get_groups():
            for student in group.get_members():
                assert student.name in grouping_string

    def test_add_group(self, students):
        new_grouping = grouper.Grouping()
        group_list = grouper.windows(students, 2)
        for group in group_list:
            new_grouping.add_group(grouper.Group(group))
        assert len(new_grouping) == 3
        assert len(new_grouping._groups[len(new_grouping) - 1]) == 2
        for group in group_list:
            new_grouping.add_group(grouper.Group(group))
        assert len(new_grouping) == 3


class TestGrouperFunctions:
    def test_slice_list_even(self):
        big_list_even = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                         17, 18]
        small_list_even = [0, 1]
        sliced = grouper.slice_list(big_list_even, 2)
        for sublist in sliced:
            assert len(sublist) == 2
        win = grouper.slice_list(big_list_even, 3)
        for i in range(0, len(win)):
            if i == (len(win) - 1):
                assert len(win[i]) <= 3
                assert len(win[i]) != 0
            else:
                assert len(win[i]) == 3
        win = grouper.slice_list(small_list_even, 2)
        assert len(win[0]) == 2
        assert len(win) == 1
        win = grouper.slice_list(small_list_even, 1)
        assert len(win) == 2

    def test_slice_list_odd(self):
        big_list_odd = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                        17]
        small_list_odd = [0]
        sliced = grouper.slice_list(big_list_odd, 2)
        for i in range(0, len(sliced)):
            if i == (len(sliced) - 1):
                assert len(sliced[i]) == 1
            else:
                assert len(sliced[i]) == 2
        win = grouper.slice_list(big_list_odd, 3)
        for i in range(0, len(win)):
            if i == (len(win) - 1):
                assert len(win[i]) <= 3
                assert len(win[i]) != 0
            else:
                assert len(win[i]) == 3
        win = grouper.slice_list(small_list_odd, 1)
        assert len(win[0]) == 2
        assert len(win) == 1
        win = grouper.slice_list(small_list_odd, 1)
        assert len(win) == 2

    def test_windows_list_even(self):
        big_list_even = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                         17, 18]
        small_list_even = [0, 1]
        window = grouper.windows(big_list_even, 2)
        for sublist in window:
            assert len(sublist) == 2
        assert len(window) == ((len(big_list_even) + 1) - 2)
        win = grouper.windows(big_list_even, 3)
        for i in range(0, len(win)):
            if i == (len(win) - 1):
                assert len(win[i]) <= 3
                assert len(win[i]) != 0
            else:
                assert len(win[i]) == 3
        win = grouper.windows(small_list_even, 2)
        assert len(win[0]) == 2
        assert len(win) == 1
        win = grouper.windows(small_list_even, 1)
        assert len(win) == 2

    def test_slice_list_odd(self):
        big_list_odd = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                        17]
        small_list_odd = [0]
        sliced = grouper.windows(big_list_odd, 2)
        assert [] not in sliced
        for i in range(0, len(sliced)):
            assert len(sliced[i]) == 2
        win = grouper.windows(big_list_odd, 3)
        for i in range(0, len(win)):
            assert len(win[i]) == 3
        win = grouper.windows(small_list_odd, 2)
        assert len(win[0]) == 1
        assert len(win) == 1
        win = grouper.slice_list(small_list_odd, 1)
        assert len(win) == 1


class TestGrouper:
    def test_make_grouping_alpha(self, questions):
        new_course = course.Course('CSC148')
        q1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                     ['Movie', 'Sing', 'Dance', 'Game'])
        new_survey = survey.Survey([q1])
        students = [course.Student(1, 'Zoro'),
                    course.Student(2, 'Aaron'),
                    course.Student(3, 'Gertrude'),
                    course.Student(4, 'Yvette'),
                    course.Student(6, 'Steph'),
                    course.Student(7, 'Draymond'),
                    course.Student(8, 'Andrew')]
        new_course.enroll_students(students)
        new_grouper = grouper.AlphaGrouper(2)
        new_grouping = new_grouper.make_grouping(new_course, new_survey)
        groups = new_grouping.get_groups()
        temp_list = []
        for i in range(0, len(groups)):
            people = groups[i].get_members()
            temp_list.extend(people)
            if i == (len(groups) - 1):
                assert len(groups[i]) <= 2
            else:
                assert len(groups[i]) == 2
        course_students = new_course.get_students()
        for student in course_students:
            assert student in temp_list

    def test_make_grouping_random(self):
        new_course = course.Course('CSC148')
        q1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                     ['Movie', 'Sing', 'Dance', 'Game'])
        new_survey = survey.Survey([q1])
        students = [course.Student(1, 'Zoro'),
                    course.Student(2, 'Aaron'),
                    course.Student(3, 'Gertrude'),
                    course.Student(4, 'Yvette'),
                    course.Student(6, 'Steph'),
                    course.Student(7, 'Draymond'),
                    course.Student(8, 'Andrew')]
        new_course.enroll_students(students)
        new_grouper = grouper.RandomGrouper(2)
        new_grouping = new_grouper.make_grouping(new_course, new_survey)
        groups = new_grouping.get_groups()
        temp_list = []
        for i in range(0, len(groups)):
            people = groups[i].get_members()
            temp_list.extend(people)
            if i == (len(groups) - 1):
                assert len(groups[i]) <= 2
            else:
                assert len(groups[i]) == 2
        course_students = new_course.get_students()
        for student in course_students:
            assert student in temp_list
        assert len(temp_list) == 7

    def test_make_grouping_greedy(self):
        new_course = course.Course('CSC148')
        q1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                     ['Movie', 'Sing', 'Dance', 'Game'])
        new_survey = survey.Survey([q1])
        students = [course.Student(1, 'Zoro'),
                    course.Student(2, 'Aaron'),
                    course.Student(3, 'Gertrude'),
                    course.Student(4, 'Yvette'),
                    course.Student(6, 'Steph'),
                    course.Student(7, 'Draymond'),
                    course.Student(8, 'Andrew')]
        new_course.enroll_students(students)
        new_grouper = grouper.GreedyGrouper(2)
        new_grouping = new_grouper.make_grouping(new_course, new_survey)
        groups = new_grouping.get_groups()
        temp_list = []
        for i in range(0, len(groups)):
            people = groups[i].get_members()
            temp_list.extend(people)
            if i == (len(groups) - 1):
                assert len(groups[i]) <= 2
            else:
                assert len(groups[i]) == 2
        course_students = new_course.get_students()
        for student in course_students:
            assert student in temp_list
        assert len(temp_list) == 7

    def test_make_grouping_window(self):
        pass


class TestHomogeneousCriterion:
    def test_score_ans(self, questions, answers):
        q1 = survey.YesNoQuestion(1, 'hey')
        h = criterion.HomogeneousCriterion()
        assert h.score_answers(q1, []) == 0.0


class TestHeterogeneousCriterion:
    def test_score_ans(self, questions, answers):
        q1 = survey.YesNoQuestion(1, 'hey')
        h = criterion.HeterogeneousCriterion()
        assert h.score_answers(q1, []) == 1.0


class TestLonelyMemberCriterion:
    def test_score_ans(self, questions, answers):
        q1 = survey.YesNoQuestion(1, 'hey')
        h = criterion.LonelyMemberCriterion()
        assert h.score_answers(q1, []) == 1.0


class TestSurvey:
    def test_len(self, questions):
        s = survey.Survey(questions)
        assert len(s) == len(s)
        assert len(s) == len(questions)

    def test_contains(self, questions):
        s = survey.Survey(questions)
        for q in questions:
            assert q in s

    def test_str(self, questions):
        s = survey.Survey(questions)
        for q in questions:
            assert str(q) in str(s)

    def test_get_questions(self, questions):
        s = survey.Survey(questions)
        s1 = survey.Survey([])
        assert s.get_questions() == questions
        assert s1.get_questions() == []

    def test_get_criterion(self, questions):
        s = survey.Survey(questions)
        for q in questions:
            assert isinstance(s._get_criterion(q),
                              criterion.HomogeneousCriterion)

    def test_get_weight(self, questions):
        s = survey.Survey(questions)
        for q in questions:
            assert isinstance(s._get_weight(q), int)
            assert s._get_weight(q) == 1

    def test_set_criterion(self, questions):
        s = survey.Survey(questions)
        for q in questions:
            s.set_criterion(criterion.LonelyMemberCriterion(), q)
        for f in questions:
            assert isinstance(s._get_criterion(f),
                              criterion.LonelyMemberCriterion)

    def test_set_weight(self, questions):
        s = survey.Survey(questions)
        for q in questions:
            s.set_weight(10000, q)
        for f in questions:
            assert s._get_weight(f) == 10000

    def test_score_students(self, questions, students_with_answers):
        s = survey.Survey(questions)
        score = s.score_students(students_with_answers)
        assert score == 2

    def test_score_grouping(self, questions, students_with_answers):
        new_course = course.Course('CSC148')
        q1 = survey.CheckboxQuestion(1, 'Hobbies?',
                                     ['Movie', 'Sing', 'Dance', 'Game'])
        new_survey = survey.Survey([q1])
        students = [course.Student(1, 'Zoro'),
                    course.Student(2, 'Aaron'),
                    course.Student(3, 'Gertrude'),
                    course.Student(4, 'Yvette'),
                    course.Student(6, 'Steph'),
                    course.Student(7, 'Draymond'),
                    course.Student(8, 'Andrew')]
        new_course.enroll_students(students_with_answers)
        new_grouper = grouper.AlphaGrouper(2)
        new_grouping = new_grouper.make_grouping(new_course, new_survey)
        s = survey.Survey(questions)
        score = s.score_grouping(new_grouping)
        assert score == 2.0

