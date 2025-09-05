def convert_to_24h(hour, minute, ampm):
  hour = int(hour)
  minute = int(minute)

  if ampm == "PM" and hour != 12:
    hour += 12
  elif ampm == "AM" and hour == 12:
    hour = 0

  return f"{hour:02}:{minute:02}:00"