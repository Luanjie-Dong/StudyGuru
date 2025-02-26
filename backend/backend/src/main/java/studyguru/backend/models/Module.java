package studyguru.backend.models;

import jakarta.persistence.*;

@Entity
@Table(name = "modules")
public class Module {
    
    @Id
    private String module_id;

    @Column(nullable = false)
    private String module_name;

    @Column(nullable = false)
    private String course_id;

    public Module() {
    }

    public Module(String module_id, String module_name, String course_id) {
        this.module_id = module_id;
        this.module_name = module_name;
        this.course_id = course_id;
    }

    public String getModule_id() {
        return module_id;
    }

    public void setModule_id(String module_id) {
        this.module_id = module_id;
    }

    public String getModule_name() {
        return module_name;
    }

    public void setModule_name(String module_name) {
        this.module_name = module_name;
    }

    public String getCourse_id() {
        return course_id;
    }

    public void setCourse_id(String course_id) {
        this.course_id = course_id;
    }

    
}
