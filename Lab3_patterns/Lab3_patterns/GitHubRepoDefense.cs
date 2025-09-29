using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class GitHubRepoDefense : ISubmissionCoursework
    {
        public void Submit(string load)
        {
            if (string.IsNullOrWhiteSpace(load)) throw new ArgumentNullException(nameof(load));

            var s = load.Trim();

            if (!s.StartsWith("https", StringComparison.OrdinalIgnoreCase) ||
                !s.EndsWith(".git", StringComparison.OrdinalIgnoreCase))
                throw new ArgumentException("Expected a string that starts with 'http' and ends with '.git'.", nameof(load));
        }
    }
}
