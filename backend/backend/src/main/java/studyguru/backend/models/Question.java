package studyguru.backend.models;

import jakarta.persistence.*;

@Entity
@Table(name="questions")
public class Question {
    @Id
    private String question_id;
    private String challenge_id;
    private int question_no;
    private QuestionDetail question_detail;
    private String input;
    private String answer;
    private String explanation;
    private String hint;
    private boolean correct;
    private int question_score;
    
    public Question(String question_id, String challenge_id, int question_no, QuestionDetail question_detail,
            String input, String answer, String explanation, String hint, boolean correct, int question_score) {
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

    public String getAnswer() {
        return answer;
    }

    public String getExplanation() {
        return explanation;
    }

    public String getHint() {
        return hint;
    }

    public boolean isCorrect() {
        return correct;
    }

    public int getQuestion_score() {
        return question_score;
    }

    
}
