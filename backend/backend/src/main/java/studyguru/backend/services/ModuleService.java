package studyguru.backend.services;

import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class ModuleService {
    
    @Value("$(module.microservice.url)")
    private String moduleMicroserviceUrl;

    public ArrayList<studyguru.backend.models.Module> getModulesByCourseId(String course_id) {
        // Endpoint
        return new ArrayList<studyguru.backend.models.Module>();
    }
}
