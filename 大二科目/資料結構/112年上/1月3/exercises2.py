def activity_selection(activities):

  activities.sort(key=lambda activity: activity[1])
  selected_activities = []
  for activity in activities:
    if not selected_activities or activity[0] >= selected_activities[-1][1]:
      selected_activities.append(activity)
  return selected_activities


if __name__ == "__main__":
  activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 8), (5, 9), (6, 10), (8, 11), (8, 12), (2, 13), (12, 14)]
  print(activity_selection(activities))