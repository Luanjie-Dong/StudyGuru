package studyguru.backend.models;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "checkpoint")
public class Checkpoint {

    @Id
    private String checkpoint_id;

    @Column(nullable = false)
    private String checkpoint_name;

    @Column(nullable = false)
    private LocalDateTime checkpoint_date;

    @Column(nullable = false)
    private String course_id;

    public Checkpoint() {
    }

    public Checkpoint(String checkpoint_id, String checkpoint_name, LocalDateTime checkpoint_date, String course_id) {
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

    public LocalDateTime getCheckpoint_date() {
        return checkpoint_date;
    }

    public void setCheckpoint_date(LocalDateTime checkpoint_date) {
        this.checkpoint_date = checkpoint_date;
    }

    public String getCourse_id() {
        return course_id;
    }

    public void setCourse_id(String course_id) {
        this.course_id = course_id;
    }
}
