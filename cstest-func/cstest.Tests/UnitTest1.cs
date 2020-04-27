using System;
using Xunit;
using Function;

namespace cstest.Tests
{
    public class UnitTest1
    {
        [Fact]
        public void Test1()
        {
            var fh = new FunctionHandler();
            var res = fh.Handle("This is my input");

            var expected = "Hi there - your input was: This is my input\n";
            
            Assert.Equal(res, expected);
            
        }
    }
}
