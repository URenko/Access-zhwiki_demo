# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from http.server import *
import http.client

class ZhwikiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.log_request()
        del self.headers['Host']
        self.headers['Host'] = 'zh.wikipedia.org'
        remote = http.client.HTTPSConnection("www.wikipedia.org")
        remote.request(self.command, self.path, headers=self.headers)
        res = remote.getresponse()
        print(res.status, res.reason)
        self.send_response(res.status, res.reason)
        for header, value in res.getheaders():
            value = value.replace('https://zh.wikipedia.org','http://127.0.0.1')
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(res.read().replace(b'https://zh.wikipedia.org',b'http://127.0.0.1').replace(b'zh.wikipedia.org',b'127.0.0.1'))
        remote.close()

server_address = ('127.0.0.1', 80)
httpd = ThreadingHTTPServer(server_address, ZhwikiHandler)
httpd.serve_forever()