package studyguru.backend.models;

public class ChallengeRequestDAO {
    private String course_id;
    private String type;
    public ChallengeRequestDAO() {
    }
    public ChallengeRequestDAO(String course_id, String type) {
        this.course_id = course_id;
        this.type = type;
    }
    public String getCourse_id() {
        return course_id;
    }
    public String getType() {
        return type;
    }
    
}
