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
