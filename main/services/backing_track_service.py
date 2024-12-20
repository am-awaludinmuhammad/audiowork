from ..utils import (
    chunk_mp3_file,
    obtain_token,
    do_the_secret_job,
    get_processed_file,
    merge_by_paths
)

def generate_backing_track(mp3_file):
    chunk_mp3 = chunk_mp3_file(mp3_file)
    chunk_paths = chunk_mp3['results']

    file_to_merge = []
    for chunk in chunk_paths:
        token_data = obtain_token(chunk.get('filepath'))
        token = token_data.get('token')
        job_data = do_the_secret_job(token)
        if job_data.get('status') == "success":
            # get the chunk backing track
            processed_file_data = get_processed_file(token)
            file_to_merge.append(processed_file_data.get('filepath'))

    merged_track = merge_by_paths(file_to_merge)
    
    return merged_track