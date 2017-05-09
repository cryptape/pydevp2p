import miniupnpc
import slogging

log = slogging.get_logger('upnp')

class UPnP(object):
  nat_upnp= None
  port = 30303
  proto = None

  def __init__(self,port,proto):
      self.nat_upnp = miniupnpc.UPnP()
      self.port = port
      self.proto = proto  
  
  def add_portmap(self):
      self.nat_upnp.discoverdelay = 200
      try:
                log.debug('Discovering... delay=%ums' % self.nat_upnp.discoverdelay)
                ndevices = self.nat_upnp.discover()
                log.debug('%u device(s) detected', ndevices)
                
                # select an igd
                self.nat_upnp.selectigd()
                # display information about the IGD and the internet connection
                log.debug('local ip address %s:', self.nat_upnp.lanaddr)
                externalipaddress = self.nat_upnp.externalipaddress()
                log.debug('external ip address %s:', externalipaddress)
                log.debug('%s %s', self.nat_upnp.statusinfo(), self.nat_upnp.connectiontype())
                log.debug('trying to redirect %s port %u %s => %s port %u %s' % (externalipaddress, self.port, self.proto,self.nat_upnp.lanaddr, self.port, self.proto))
                mapping = self.nat_upnp.getspecificportmapping(self.port, self.proto)
                log.debug('mapping return %s',mapping)
                if mapping != None: 
                   raise Exception('Port %u is already mapped' % self.port)
                else:
                   b = self.nat_upnp.addportmapping(self.port, self.proto, self.nat_upnp.lanaddr, self.port,
                            'UPnP IGD port %u' % self.port, '')
                   if b:
                        log.info('Success. Now waiting for %s request on %s:%u' % (self.proto,externalipaddress,self.port))
                   else:
                        log.debug('Failed')
        except Exception as e:
                log.debug('Exception :%s', e)


  def delete_portmap(self):
      try:
                b = self.nat_upnp.deleteportmapping(self.port, self.proto)
                if b:
                        log.debug('Successfully deleted port mapping %u %s' % (self.port, self.proto))
                else:
                        log.debug('Failed to remove port mapping')
      except Exception as e:
                log.debug('Exception :%s', e)
