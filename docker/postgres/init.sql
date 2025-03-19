-- Enable pg_cron extension
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Schedule the soft delete job (runs daily at midnight)
SELECT cron.schedule(
    'soft_delete_old_movies',
    '0 0 * * *',  -- Runs daily at midnight
    $$
    UPDATE movies
    SET 
        title = NULL,
        genres = NULL,
        overview = NULL,
        release_date = NULL,
        vote_average = NULL,
        vote_count = NULL,
        runtime = NULL,
        tagline = NULL,
        keywords = NULL,
        poster_path = NULL,
        backdrop_path = NULL,
        images_path = NULL
    WHERE created_at < NOW() - INTERVAL '6 months'
    $$
);

-- Schedule a job to clean up old cache entries (runs daily at midnight)
SELECT cron.schedule(
    'delete_old_cache_entries',
    '0 0 * * *',  -- Runs daily at midnight
    $$
    DELETE FROM cache
    WHERE updated_at IS NOT NULL 
      AND updated_at < NOW() - INTERVAL '6 months'
    $$
);