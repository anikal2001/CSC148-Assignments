"""CSC148 Assignment 1

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Misha Schwartz, Mario Badr, Christine Murad, Diane Horton, Sophia Huynh
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Misha Schwartz, Mario Badr, Christine Murad, Diane Horton,
Sophia Huynh and Jaisie Sin

=== Module Description ===

This file contains classes that describe a survey as well as classes that
described different types of questions that can be asked in a given survey.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Union, Dict, List
from criterion import HomogeneousCriterion, InvalidAnswerError

if TYPE_CHECKING:
    from criterion import Criterion
    from grouper import Grouping
    from course import Student


class Question:
    """ An abstract class representing a question used in a survey

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """

    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """ Initialize a question with the text <text> """
        self.id = id_
        self.text = text

    def __str__(self) -> str:
        """
        Return a string representation of this question that contains both
        the text of this question and a description of all possible answers
        to this question.

        You can choose the precise format of this string.
        """
        raise NotImplementedError

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff <answer> is a valid answer to this question.
        """
        raise NotImplementedError

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """ Return a float between 0.0 and 1.0 indicating how similar two
        answers are.

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question
        """
        raise NotImplementedError


class MultipleChoiceQuestion(Question):
    """ A question whose answers can be one of several options

    === Public Attributes ===
    id: the id of this question
    text: the text of this question
    options: list of possible answers to the MultipleChoiceQuestion

    === Representation Invariants ===
    text is not the empty string
    """

    id: int
    text: str
    options: List[str]

    def __init__(self, id_: int, text: str, options: List[str]) -> None:
        """
        Initialize a question with the text <text> and id <id> and
        possible answers <options>.

        === Precondition ===
        No two elements in <options> are the same string
        <options> contains at least two elements
        """
        Question.__init__(self, id_, text)
        self.options = options

    def __str__(self) -> str:
        """
        Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return 'Question: {0} \n Options: {1}' \
            .format(self.text, str(self.options))

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff <answer> is a valid answer to this question.

        An answer is valid if its content is one of the possible answers to this
        question.
        """
        for option in self.options:
            if option == answer.content:
                return True
        return False

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """
        Return 1.0 iff <answer1>.content and <answer2>.content are equal and
        0.0 otherwise.

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question.
        """
        if answer1.content == answer2.content:
            return 1.0
        else:
            return 0.0
        # TODO: should this be implemented in parent class????


class NumericQuestion(Question):
    """ A question whose answer can be an integer between some
    minimum and maximum value (inclusive).

    === Public Attributes ===
    id: the id of this question
    text: the text of this question
    min: the minimum bound of the Answer
    max: the maximum bound of the Answer

    === Representation Invariants ===
    text is not the empty string
    """

    id: int
    text: str
    min: int
    max: int

    def __init__(self, id_: int, text: str, min_: int, max_: int) -> None:
        """
        Initialize a question with id <id_> and text <text> whose possible
        answers can be any integer between <min_> and <max_> (inclusive)

        === Precondition ===
        min_ < max_
        """
        Question.__init__(self, id_, text)
        self.min = min_
        self.max = max_

    def __str__(self) -> str:
        """
        Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return 'Question: {0} \n Answer is an integer between {1} and {2}' \
            .format(self.text, self.min, self.max)

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff the content of <answer> is an integer between the
        minimum and maximum (inclusive) possible answers to this question.
        """
        content = answer.content
        return isinstance(content, int) and self.min <= content <= self.max

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """
        Return the similarity between <answer1> and <answer2> over the range
        of possible answers to this question.

        Similarity calculated by:

        1. first find the absolute difference between <answer1>.content and
           <answer2>.content.
        2. divide the value from step 1 by the difference between the maximimum
           and minimum possible answers.
        3. subtract the value from step 2 from 1.0

        Hint: this is the same calculation from the worksheet in lecture!

        For example:
        - Maximum similarity is 1.0 and occurs when <answer1> == <answer2>
        - Minimum similarity is 0.0 and occurs when <answer1> is the minimum
            possible answer and <answer2> is the maximum possible answer
            (or vice versa).

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question
        """
        difference = abs(answer1.content - answer2.content)
        mark = difference / (self.max - self.min)
        new_mark = 1.0 - mark
        return new_mark


class YesNoQuestion(Question):
    """ A question whose answer is either yes (represented by True) or
    no (represented by False).

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """
        Initialize a question with the text <text> and id <id>.
        """
        Question.__init__(self, id_, text)

    def __str__(self) -> str:
        """
        Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return 'Question: {0} \n Answer is either \'True\' or \'False\'' \
            .format(self.text)

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff <answer>'s content is a boolean.
        """
        return isinstance(answer.content, bool)

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """
        Return 1.0 iff <answer1>.content is equal to <answer2>.content and
        return 0.0 otherwise.

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question
        """
        if answer1.content == answer2.content:
            return 1.0
        else:
            return 0.0


class CheckboxQuestion(MultipleChoiceQuestion):
    """ A question whose answers can be one or more of several options

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """

    id: int
    text: str
    options: List[str]

    def __init__(self, id_: int, text: str, options: List[str]) -> None:
        "Initialize a Checkbox Question"
        MultipleChoiceQuestion.__init__(self, id_, text, options)
        # TODO: CHECK IF INIT NEEDS TO BE CALLED

    def __str__(self) -> str:
        """
        Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return 'Question: {0} \n Answer could be one or more of these options: \
        {1}'.format(self.text, str(self.options))

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff <answer> is a valid answer to this question.

        An answer is valid iff its content is a non-empty list containing
        unique possible answers to this question.
        """
        content = answer.content
        if isinstance(content, list) and len(content) > 0:
            for possible in content:
                if (content.count(possible) > 1) or \
                        (possible not in self.options):
                    return False
            return True
        return False

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """
        Return the similarity between <answer1> and <answer2>.

        Similarity is defined as the ratio between the number of strings that
        are common to both <answer1>.content and <answer2>.content over the
        total number of unique strings that appear in both <answer1>.content and
        <answer2>.content

        For example, if <answer1>.content == ['a', 'b', 'c'] and
        <answer1>.content == ['c', 'b', 'd'], the strings that are common to
        both are ['c', 'b'] and the unique strings that appear in both are
        ['a', 'b', 'c', 'd'].

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question
        """
        common = 0
        unique_list = set(answer1.content + answer2.content)
        unique = len(unique_list)

        for answer in answer1.content:
            if answer in answer2.content:
                common += 1

        return common / unique


class Answer:
    """ An answer to a question used in a survey

    === Public Attributes ===
    content: an answer to a single question
    """
    content: Union[str, bool, int, List[str]]

    def __init__(self,
                 content: Union[str, bool, int, List[Union[str]]]) -> None:
        """Initialize an answer with content <content>"""
        self.content = content

    def is_valid(self, question: Question) -> bool:
        """Return True iff self.content is a valid answer to <question>"""
        return question.validate_answer(self)


class Survey:
    """
    A survey containing questions as well as criteria and weights used to
    evaluate the quality of a group based on their answers to the survey
    questions.

    === Private Attributes ===
    _questions: a dictionary mapping each question's id to the question itself
    _criteria: a dictionary mapping a question's id to its associated criterion
    _weights: a dictionary mapping a question's id to a weight; an integer
              representing the importance of this criteria.
    _default_criterion: a criterion to use to evaluate a question if the
              question does not have an associated criterion in _criteria
    _default_weight: a weight to use to evaluate a question if the
              question does not have an associated weight in _weights

    === Representation Invariants ===
    No two questions on this survey have the same id
    Each key in _questions equals the id attribute of its value
    Each key in _criteria occurs as a key in _questions
    Each key in _weights occurs as a key in _questions
    Each value in _weights is greater than 0
    _default_weight > 0
    """

    _questions: Dict[int, Question]
    _criteria: Dict[int, Criterion]
    _weights: Dict[int, int]
    _default_criterion: Criterion
    _default_weight: int

    def __init__(self, questions: List[Question]) -> None:
        """
        Initialize a new survey that contains every question in <questions>.
        This new survey should use a HomogeneousCriterion as a default criterion
        and should use 1 as a default weight.
        """
        self._questions = {}
        self._weights = {}
        self._criteria = {}
        self._default_criterion = HomogeneousCriterion()
        self._default_weight = 1

        if len(questions) > 0:
            for question in questions:
                self._questions[question.id] = question

    def __len__(self) -> int:
        """ Return the number of questions in this survey """
        return len(self._questions)

    def __contains__(self, question: Question) -> bool:
        """
        Return True iff there is a question in this survey with the same
        id as <question>.
        """
        return question.id in self._questions

    def __str__(self) -> str:
        """
        Return a string containing the string representation of all
        questions in this survey

        You can choose the precise format of this string.
        """
        string = 'Questions:'
        ques_list = self.get_questions()
        for ques in ques_list:
            string += str(ques)
        return string

    def get_questions(self) -> List[Question]:
        """ Return a list of all questions in this survey """
        ques_list = []
        for ques_id in self._questions:
            ques_list.append(self._questions[ques_id])
        return ques_list

    def _get_criterion(self, question: Question) -> Criterion:
        """
        Return the criterion associated with <question> in this survey.

        Iff <question>.id does not appear in self._criteria, return the default
        criterion for this survey instead.

        === Precondition ===
        <question>.id occurs in this survey
        """
        if question.id in self._criteria:
            return self._criteria[question.id]
        else:
            return self._default_criterion

    def _get_weight(self, question: Question) -> int:
        """
        Return the weight associated with <question> in this survey.

        Iff <question>.id does not appear in self._weights, return the default
        weight for this survey instead.

        === Precondition ===
        <question>.id occurs in this survey
        """
        if question.id in self._weights:
            return self._weights.get(question.id)
        else:
            return self._default_weight

    def set_weight(self, weight: int, question: Question) -> bool:
        """
        Set the weight associated with <question> to <weight> and return True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        if (question.id in self._questions) and (weight > 0):
            self._weights[question.id] = weight
            return True
        else:
            return False

    def set_criterion(self, criterion: Criterion, question: Question) -> bool:
        """
        Set the criterion associated with <question> to <criterion> and return
        True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        if question.id in self._questions:
            self._criteria[question.id] = criterion
            return True
        else:
            return False

    def score_students(self, students: List[Student]) -> float:
        """
        Return a quality score for <students> calculated based on their answers
        to the questions in this survey, and the associated criterion and weight
        for each question .

        This score is determined using the following algorithm:

        1. For each question in <self>, find its associated criterion, weight,
           and <students> answers to this question. Use the score_answers method
           for this criterion to calculate a quality score. Multiply this
           quality score by the associated weight.
        2. Find the average of all quality scores from step 1.

        If an InvalidAnswerError would be raised by calling this method, or if
        there are no questions in <self>, this method should return zero.

        === Precondition ===
        All students in <students> have an answer to all questions in this
            survey
        """
        score = 0.0
        count = 0

        for qid in self._questions:
            if qid in self._criteria:
                criterion = self._criteria[qid]
            else:
                criterion = self._default_criterion

            if qid in self._weights:
                weight = self._weights[qid]
            else:
                weight = self._default_weight

            answer_list = []
            for student in students:
                answer_list.append(student.get_answer(self._questions[qid]))

            try:
                qs = criterion.score_answers(self._questions[qid], answer_list)
            except InvalidAnswerError:
                return 0.0
            else:
                weighted = qs * weight
                score += weighted
                count += 1

        if count == 0:
            return 0.0
        return score / count

    def score_grouping(self, grouping: Grouping) -> float:
        """ Return a score for <grouping> calculated based on the answers of
        each student in each group in <grouping> to the questions in <self>.

        If there are no groups in <grouping> this score is 0.0. Otherwise, this
        score is determined using the following algorithm:

        1. For each group in <grouping>, get the score for the members of this
           group calculated based on their answers to the questions in this
           survey.
        2. Return the average of all the scores calculated in step 1.

        === Precondition ===
        All students in the groups in <grouping> have an answer to all questions
            in this survey
        """
        score = 0.0
        count = 0
        group_list = grouping.get_groups()

        for group in group_list:
            student_list = group.get_members()
            score += self.score_students(student_list)
            count += 1

        if count == 0:
            return 0.0
        return score / count


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'criterion',
                                                  'course',
                                                  'grouper']})
