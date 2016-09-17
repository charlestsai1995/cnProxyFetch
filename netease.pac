function FindProxyForURL(url, host) {
   if (host == 'music.163.com') return 'PROXY 120.52.72.58:80';
   if (shExpMatch(url,"*.xiami.com/*")) return 'PROXY 120.52.72.58:80';
   if (shExpMatch(url,"*.xiami.net/*")) return 'PROXY 120.52.72.58:80';
   if (shExpMatch(url,"*.cnzz.com/*")) return 'PROXY 120.52.72.58:80';
   if (shExpMatch(url,"*.tudou.com/*")) return 'PROXY 120.52.72.58:80';
   return 'DIRECT';
}
//2016-09-17 02:29:02
