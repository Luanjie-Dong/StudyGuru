package studyguru.backend.models;

import java.time.OffsetDateTime;

public class Checkpoint {

    private String checkpoint_id;

    private String checkpoint_name;

    private OffsetDateTime checkpoint_date;

    private String course_id;

    public Checkpoint() {
    }

    public Checkpoint(String checkpoint_id, String checkpoint_name, OffsetDateTime checkpoint_date, String course_id) {
        this.checkpoint_id = checkpoint_id;
        this.checkpoint_name = checkpoint_name;
        this.checkpoint_date = checkpoint_date;
        this.course_id = course_id;
    }

    public String getCheckpoint_id() {
        return checkpoint_id;
    }

    public void setCheckpoint_id(String checkpoint_id) {
        this.checkpoint_id = checkpoint_id;
    }

    public String getCheckpoint_name() {
        return checkpoint_name;
    }

    public void setCheckpoint_name(String checkpoint_name) {
        this.checkpoint_name = checkpoint_name;
    }

    public OffsetDateTime getCheckpoint_date() {
        return checkpoint_date;
    }

    public void setCheckpoint_date(OffsetDateTime checkpoint_date) {
        this.checkpoint_date = checkpoint_date;
    }

    public String getCourse_id() {
        return course_id;
    }

    public void setCourse_id(String course_id) {
        this.course_id = course_id;
    }
}
