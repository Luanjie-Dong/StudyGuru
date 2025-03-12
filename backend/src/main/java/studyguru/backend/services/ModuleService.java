package studyguru.backend.services;

import java.util.ArrayList;
import java.util.Arrays;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class ModuleService {
    
    @Value("${module.microservice.url}")
    private String moduleMicroserviceUrl;

    private RestTemplate restTemplate = new RestTemplate();

    public ArrayList<studyguru.backend.models.Module> getModulesByCourseId(String course_id) {
        ResponseEntity<studyguru.backend.models.Module[]> response = restTemplate.getForEntity(moduleMicroserviceUrl + "/module?course_id=" + course_id, studyguru.backend.models.Module[].class);
        studyguru.backend.models.Module[] modules = response.getBody();
        return modules != null ? new ArrayList<>(Arrays.asList(modules)) : new ArrayList<>();
    }
}
