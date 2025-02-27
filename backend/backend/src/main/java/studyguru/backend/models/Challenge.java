package studyguru.backend.models;

import java.time.LocalDateTime;
import java.util.ArrayList;

enum Type {
    DAILY,
    CHECKPOINT
}

public class Challenge {
    private String challenge_id;
    private String course_id;
    private Type type;
    private int challenge_score;
    private LocalDateTime start_datetime;
    private LocalDateTime end_datetime;
    private ArrayList<String> modules;

    public Challenge(String challenge_id, String course_id, Type type, int challenge_score,
            LocalDateTime start_datetime, LocalDateTime end_datetime, ArrayList<String> modules) {
        this.challenge_id = challenge_id;
        this.course_id = course_id;
        this.type = type;
        this.challenge_score = challenge_score;
        this.start_datetime = start_datetime;
        this.end_datetime = end_datetime;
        this.modules = modules;
    }

    public String getChallenge_id() {
        return challenge_id;
    }

    public String getCourse_id() {
        return course_id;
    }

    public Type getType() {
        return type;
    }

    public int getChallenge_score() {
        return challenge_score;
    }

    public LocalDateTime getStart_datetime() {
        return start_datetime;
    }

    public LocalDateTime getEnd_datetime() {
        return end_datetime;
    }

    public ArrayList<String> getModules() {
        return modules;
    }

    
}
