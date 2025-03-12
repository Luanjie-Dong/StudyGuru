package studyguru.backend.models;

import java.util.*;
import com.fasterxml.jackson.annotation.JsonFormat;

public class Question {
    private String question_id;
    private String challenge_id;
    private int question_no;
    private QuestionDetail question_detail;
    private String input;
    @JsonFormat(with = JsonFormat.Feature.ACCEPT_SINGLE_VALUE_AS_ARRAY)
    private List<String> answer;
    private String explanation;
    private String hint;
    private Boolean correct; // changed from boolean to Boolean
    private int question_score;
    
    // Added default constructor for Jackson deserialization
    public Question() { }

    public Question(String question_id, String challenge_id, int question_no, QuestionDetail question_detail,
            String input, List<String> answer, String explanation, String hint, Boolean correct, int question_score) {
        this.question_id = question_id;
        this.challenge_id = challenge_id;
        this.question_no = question_no;
        this.question_detail = question_detail;
        this.input = input;
        this.answer = answer;
        this.explanation = explanation;
        this.hint = hint;
        this.correct = correct;
        this.question_score = question_score;
    }

    public String getQuestion_id() {
        return question_id;
    }

    public String getChallenge_id() {
        return challenge_id;
    }

    public int getQuestion_no() {
        return question_no;
    }

    public QuestionDetail getQuestion_detail() {
        return question_detail;
    }

    public String getInput() {
        return input;
    }

    public List<String> getAnswer() {
        return answer;
    }

    public String getExplanation() {
        return explanation;
    }

    public String getHint() {
        return hint;
    }

    public Boolean isCorrect() {
        return correct;
    }

    public int getQuestion_score() {
        return question_score;
    }

    
}
