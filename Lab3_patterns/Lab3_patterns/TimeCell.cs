using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class TimeCell
    {
        public DayOfWeek Day { get; }
        public TimeOnly Start { get; }
        public TimeOnly End { get; }


        public TimeCell(DayOfWeek day, TimeOnly start, TimeOnly end)
        {
            if (end <= start) throw new ArgumentException("End must be after Start");
            this.Day = day;
            this.Start = start;
            this.End = end;
        }

        public bool CheckOverlay(TimeCell other)
        {
            if (Day != other.Day) return false;
            return Start < other.Start && End < other.End;
        }
        public static TimeCell Parse(DayOfWeek day, string start, string end)
        {
            var s = TimeOnly.Parse(start, CultureInfo.InvariantCulture);
            var e = TimeOnly.Parse(end, CultureInfo.InvariantCulture);
            return new TimeCell(day, s, e);
        }
    }
}
