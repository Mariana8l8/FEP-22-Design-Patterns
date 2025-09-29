using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public abstract class Coursework
    {
        public string Title { get; }
        public ISubmissionCoursework TypeOfDefenseSubmission { get; }
        public ISuperviseCapable Supervisor { get; }


        protected Coursework(string title, ISubmissionCoursework typeOfDefenseSubmission, ISuperviseCapable supervisor)
        {
            Title = title ?? throw new ArgumentNullException(nameof(title));
            Supervisor = supervisor ?? throw new ArgumentNullException(nameof(supervisor));
            TypeOfDefenseSubmission = typeOfDefenseSubmission ?? throw new ArgumentNullException(nameof(typeOfDefenseSubmission));
        }
        public abstract void Submit(List<string> load);
    }
}
