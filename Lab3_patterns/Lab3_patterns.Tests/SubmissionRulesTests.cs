using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns.Tests
{
    public class SubmissionRulesTests
    {
        [Theory]
        //[InlineData("file.txt")]
        //[InlineData("report.docx")]
        //[InlineData("image.png")]
        //[InlineData("justname")]     
        [InlineData(".pdf")]
        public void CheckOnlineSubmission_ForCorrectlyMarksAFile(string fileName)
        {
            ISubmissionCoursework submission = new OnlineUploadDefense();

            var ex = Record.Exception(() => submission.Submit(fileName));
            Assert.Null(ex);

            //Assert.Throws<ArgumentException>(() => submission.Submit(fileName));
        }

        [Theory]
        //[InlineData("file.txt")]
        //[InlineData("report.docx")]
        //[InlineData("justname")]
        //[InlineData(".pdf")]
        [InlineData("https: //github.com/.git")]
        public void CheckGitHubSubmission_ForCorrectlyRepositoryLink(string fileName)
        {
            ISubmissionCoursework submission = new GitHubRepoDefense();

            var ex = Record.Exception(() => submission.Submit(fileName));
            Assert.Null(ex);

            //Assert.Throws<ArgumentException>(() => submission.Submit(fileName));
        }
    }
}
