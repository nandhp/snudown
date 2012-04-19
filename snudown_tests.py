import snudown
import unittest

class SnudownTest(unittest.TestCase):
    testdata = {}
    def runTest(self):
        for md,html in self.testdata:
            self.assertEqual(snudown.markdown(md), html)

class TestSubredditAndUsernameAutolinking(SnudownTest):
    testdata = []

    def __init__(self, methodName='runTest'):
        SnudownTest.__init__(self, methodName)

        # These strings will be autolinked
        ok = [
            # Subreddits
            '/r/ca', '/r/abc', '/r/t:y', '/r/reddit.com', '/r/1984sweet1984',
            '/r/fffffffuuuuuuuuuuuu01',
            '/r/funny+pics', '/r/reddit.com+funny+AskReddit',
            '/r/t:yesterday+t:tommorow', '/r/reddit.com+funny+t:tommorow',
            '/r/t:tommorow+funny+reddit.com',
            # Usernames
            '/u/abc', '/u/_username'
        ]
        # These strings will not be autolinked
        notok = [
            # Subreddits
            '/r/', '/r/!',
            '/r/a', '/r/t', '/r/t', '/r/t:', '/r/a:', '/r/a:b',
            '/r/a:bcd',
            '/r/reddit.comx',
            '/r/fffffffuuuuuuuuuuuu012',
            '/r/funny+reddit.comx+abc', '/r/funny+r:ome',
            '/r/foo+', '/r/+foo', '/r/foo++bar',
            # Usernames
            '/u/', '/u/!'
        ]

        # Generate the test list using various prefixes and suffixes
        for x in ok:
            xl = '<a href="' + x + '">' + x + '</a>'
            for pre,suf in (('',''),('abc ',' def'),('abc',', def')):
                self.testdata.append((pre+x+suf, '<p>'+pre+xl+suf+'</p>\n'))
        for x in notok:
            for pre,suf in (('',''),('abc ',' def')):
                self.testdata.append((pre+x+suf, '<p>'+pre+x+suf+'</p>\n'))

if __name__ == '__main__':
    unittest.main()
