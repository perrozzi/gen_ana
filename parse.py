from BetterConfigParser import BetterConfigParser
from collections import defaultdict

class samples(object):
    def __init__(self,config):
        self.samples = []
        self.config = BetterConfigParser()
        self.config.read(config)
        for section in self.config.sections():
            # empty object :)
            self.samples.append(lambda:sample)
            for key, value in self.config.items(section):
                setattr(self.samples[-1],key,value)

    def __getattr__(self, key):
        l = []
        for x in self.samples:
            l.append((getattr(x,key),x))
        def_dict = defaultdict(list)
        for k,v in l:
            def_dict[k].append(v)
        return def_dict

    def __getitem__(self, key):
        return [getattr(x,key) for x in self.samples]
        #return filter(lambda x: x.key == value, self.samples)

                

if __name__ == '__main__':
    import sys
    file = sys.argv[1]
    s = samples(file)
    print s['process']
    print s['xsec']
    for bla in s.group['DY']:
        print bla.xsec
