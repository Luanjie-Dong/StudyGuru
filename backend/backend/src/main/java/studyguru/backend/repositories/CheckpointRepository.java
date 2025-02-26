// package studyguru.backend.repositories;

// import org.springframework.data.jpa.repository.JpaRepository;
// import org.springframework.stereotype.Repository;
// import studyguru.backend.models.Checkpoint;

// import java.time.LocalDateTime;
// import java.util.List;

// @Repository
// public interface CheckpointRepository extends JpaRepository<Checkpoint, String> {

//     // Find checkpoints by exact date (ignoring time)
//     List<Checkpoint> findByCheckpointDateBetween(LocalDateTime startOfDay, LocalDateTime endOfDay);
// }
