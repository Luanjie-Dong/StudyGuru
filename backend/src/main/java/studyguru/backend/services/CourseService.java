package studyguru.backend.services;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import studyguru.backend.models.Course;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Service
public class CourseService {

    @Value("$(course.microservice.url)")
    private String courseMicroserviceUrl;
    
    private RestTemplate restTemplate;

    public List<Course> getAllCourses() {
        ResponseEntity<Course[]> response = restTemplate.getForEntity(courseMicroserviceUrl + "/course", Course[].class);
        Course[] courses = response.getBody();
        return courses != null ? Arrays.asList(courses) : new ArrayList<>();
    }
    
}
