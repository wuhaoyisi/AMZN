def find_champion_photo(photos, compare):
    # photos: list of photo objects or indices
    # compare: function that returns True if photoA beats photoB
    
    n = len(photos)
    if n == 0:
        return None  # no photos to compare
    if n == 1:
        return photos[0]  # single photo is champion by default
    
    # track how many times each photo loses (indegree in tournament graph)
    loss_count = [0] * n  # indegree array, loss_count[i] = number of photos that beat photo i
    
    # build tournament graph by comparing every pair of photos
    for i in range(n):
        for j in range(i + 1, n):  # avoid duplicate comparisons since tournament is complete
            # compare photo i with photo j to determine winner
            if compare(photos[i], photos[j]):
                # photo i beats photo j, so j gets a loss
                loss_count[j] += 1
            else:
                # photo j beats photo i, so i gets a loss  
                loss_count[i] += 1
    
    # find photos that were never beaten (indegree = 0)
    champion_candidates = []
    for i in range(n):
        if loss_count[i] == 0:  # photo i beat all other photos
            champion_candidates.append(i)
    
    # handle different scenarios based on number of champions found
    if len(champion_candidates) == 1:
        return photos[champion_candidates[0]]  # unique champion found
    elif len(champion_candidates) == 0:
        # no champion exists (circular dominance), return photo with minimum losses
        min_losses = min(loss_count)
        best_photo_index = loss_count.index(min_losses)
        return photos[best_photo_index]
    else:
        # multiple champions (should not happen in valid tournament), return first one
        return photos[champion_candidates[0]]
