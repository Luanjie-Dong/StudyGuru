package studyguru.backend.services;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import studyguru.backend.models.Course;

import java.util.ArrayList;
import java.util.List;

@Service
public class CourseService {

    @Value("$(course.microservice.url)")
    private String courseMicroserviceUrl;

    public List<Course> getAllCourses() {
        return new ArrayList<Course>();
    }
    
}
