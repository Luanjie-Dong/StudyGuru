package studyguru.backend.models;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "course")
public class Course {

    @Id
    private String course_id;

    @Column(nullable = false)
    private String userId;

    @Column(nullable = false)
    private String course_name;

    private int streak;

    private LocalDateTime created_at;

    private String latest_module_id;

    public Course() {
    }

    public Course(String course_id, String userId, String course_name, int streak, LocalDateTime created_at,
                  String latest_module_id) {
        this.course_id = course_id;
        this.userId = userId;
        this.course_name = course_name;
        this.streak = streak;
        this.created_at = created_at;
        this.latest_module_id = latest_module_id;
    }

    public String getCourse_id() {
        return course_id;
    }

    public void setCourse_id(String course_id) {
        this.course_id = course_id;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getCourse_name() {
        return course_name;
    }

    public void setCourse_name(String course_name) {
        this.course_name = course_name;
    }

    public int getStreak() {
        return streak;
    }

    public void setStreak(int streak) {
        this.streak = streak;
    }

    public LocalDateTime getCreated_at() {
        return created_at;
    }

    public void setCreated_at(LocalDateTime created_at) {
        this.created_at = created_at;
    }

    public String getLatest_module_id() {
        return latest_module_id;
    }

    public void setLatest_module_id(String latest_module_id) {
        this.latest_module_id = latest_module_id;
    }
}
