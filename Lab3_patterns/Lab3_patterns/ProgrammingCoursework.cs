using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class ProgrammingCoursework : Coursework
    {
        public ProgrammingCoursework(string title, ISubmissionCoursework typeOfDefenseSubmission, ISuperviseCapable supervisor) : base(title, typeOfDefenseSubmission, supervisor) { }
        public override void Submit(List<string> load)
        {
            if (load is null) throw new ArgumentNullException(nameof(load));
        }
    }
}
