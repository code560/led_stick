# frozen_string_literal: true

require 'fiddle/import'

##
# libbcm2835
module BCM
  extend Fiddle::Importer
  dlload '/usr/local/lib/libbcm2835.so'
  extern 'int bcm2835_init(void)'
  extern 'int bcm2835_close(void)'
  extern 'void  bcm2835_set_debug(unsigned char debug)'
  extern 'unsigned int bcm2835_version(void)'
  extern 'unsigned int* bcm2835_regbase(unsigned char regbase)'
  extern 'unsigned int bcm2835_peri_read(volatile unsigned int* paddr)'
  extern 'unsigned int bcm2835_peri_read_nb(volatile unsigned int* paddr)'
  extern 'void bcm2835_peri_write(volatile unsigned int* paddr, unsigned int value)'
  extern 'void bcm2835_peri_write_nb(volatile unsigned int* paddr, unsigned int value)'
  extern 'void bcm2835_peri_set_bits(volatile unsigned int* paddr, unsigned int value, unsigned int mask)'
  extern 'void bcm2835_gpio_fsel(unsigned char pin, unsigned char mode)'
  extern 'void bcm2835_gpio_set(unsigned char pin)'
  extern 'void bcm2835_gpio_clr(unsigned char pin)'
  extern 'void bcm2835_gpio_set_multi(unsigned int mask)'
  extern 'void bcm2835_gpio_clr_multi(unsigned int mask)'
  extern 'unsigned char bcm2835_gpio_lev(unsigned char pin)'
  extern 'unsigned char bcm2835_gpio_eds(unsigned char pin)'
  extern 'void bcm2835_gpio_set_eds(unsigned char pin)'
  extern 'void bcm2835_gpio_ren(unsigned char pin)'
  extern 'void bcm2835_gpio_clr_ren(unsigned char pin)'
  extern 'void bcm2835_gpio_fen(unsigned char pin)'
  extern 'void bcm2835_gpio_clr_fen(unsigned char pin)'
  extern 'void bcm2835_gpio_hen(unsigned char pin)'
  extern 'void bcm2835_gpio_clr_hen(unsigned char pin)'
  extern 'void bcm2835_gpio_len(unsigned char pin)'
  extern 'void bcm2835_gpio_clr_len(unsigned char pin)'
  extern 'void bcm2835_gpio_aren(unsigned char pin)'
  extern 'void bcm2835_gpio_clr_aren(unsigned char pin)'
  extern 'void bcm2835_gpio_afen(unsigned char pin)'
  extern 'void bcm2835_gpio_clr_afen(unsigned char pin)'
  extern 'void bcm2835_gpio_pud(unsigned char pud)'
  extern 'void bcm2835_gpio_pudclk(unsigned char pin, unsigned char on)'
  extern 'unsigned int bcm2835_gpio_pad(unsigned char group)'
  extern 'void bcm2835_gpio_set_pad(unsigned char group, unsigned int control)'
  extern 'void bcm2835_delay (unsigned int millis)'
  extern 'void bcm2835_delayMicroseconds (unsigned long long micros)'
  extern 'void bcm2835_gpio_write(unsigned char pin, unsigned char on)'
  extern 'void bcm2835_gpio_write_multi(unsigned int mask, unsigned char on)'
  extern 'void bcm2835_gpio_write_mask(unsigned int value, unsigned int mask)'
  extern 'void bcm2835_gpio_set_pud(unsigned char pin, unsigned char pud)'
  extern 'void bcm2835_spi_begin(void)'
  extern 'void bcm2835_spi_end(void)'
  extern 'void bcm2835_spi_setBitOrder(unsigned char order)'
  extern 'void bcm2835_spi_setClockDivider(unsigned short divider)'
  extern 'void bcm2835_spi_setDataMode(unsigned char mode)'
  extern 'void bcm2835_spi_chipSelect(unsigned char cs)'
  extern 'void bcm2835_spi_setChipSelectPolarity(unsigned char cs, unsigned char active)'
  extern 'unsigned char bcm2835_spi_transfer(unsigned char value)'
  extern 'void bcm2835_spi_transfernb(char* tbuf, char* rbuf, unsigned int len)'
  extern 'void bcm2835_spi_transfern(char* buf, unsigned int len)'
  extern 'void bcm2835_spi_writenb(char* buf, unsigned int len)'
  extern 'void bcm2835_i2c_begin(void)'
  extern 'void bcm2835_i2c_end(void)'
  extern 'void bcm2835_i2c_setSlaveAddress(unsigned char addr)'
  extern 'void bcm2835_i2c_setClockDivider(unsigned short divider)'
  extern 'void bcm2835_i2c_set_baudrate(unsigned int baudrate)'
  extern 'unsigned char bcm2835_i2c_write(const char * buf, unsigned int len)'
  extern 'unsigned char bcm2835_i2c_read(char* buf, unsigned int len)'
  extern 'unsigned char bcm2835_i2c_read_register_rs(char* regaddr, char* buf, unsigned int len)'
  extern 'unsigned char bcm2835_i2c_write_read_rs(char* cmds, unsigned int cmds_len, char* buf, unsigned int buf_len)'
  extern 'unsigned long long bcm2835_st_read(void)'
  extern 'void bcm2835_st_delay(unsigned long long offset_micros, unsigned long long micros)'
  extern 'void bcm2835_pwm_set_clock(unsigned int divisor)'
  extern 'void bcm2835_pwm_set_mode(unsigned char channel, unsigned char markspace, unsigned char enabled)'
  extern 'void bcm2835_pwm_set_range(unsigned char channel, unsigned int range)'
  extern 'void bcm2835_pwm_set_data(unsigned char channel, unsigned int data)'
end

##
# SPI wrapper
module SPI
  CS0 = 0
  CS1 = 1
  @mutex = Mutex.new

  ##
  # @param array tx data
  # @param cs chip select (CS0 or CS1)
  def write(array, cs)
    @mutex.synchronize do
      BCM.bcm2835_spi_begin
      BCM.bcm2835_spi_setBitOrder(1) # MSB First
      BCM.bcm2835_spi_setDataMode(0) # CPOL = 0, CPHA = 0
      BCM.bcm2835_spi_setClockDivider(128)
      BCM.bcm2835_spi_chipSelect(cs)
      BCM.bcm2835_spi_setChipSelectPolarity(cs, 0) # LOW
      BCM.bcm2835_spi_writenb(array, array.size)
      BCM.bcm2835_spi_end
    end
  end

  def read_write(array, cs)
    @mutex.synchronize do
      buffer = ([0] * array.size).pack('c*')
      BCM.bcm2835_spi_begin
      BCM.bcm2835_spi_setBitOrder(1) # MSB First
      BCM.bcm2835_spi_setDataMode(0) # CPOL = 0, CPHA = 0
      BCM.bcm2835_spi_setClockDivider(128)
      BCM.bcm2835_spi_chipSelect(cs)
      BCM.bcm2835_spi_setChipSelectPolarity(cs, 0) # LOW
      BCM.bcm2835_spi_transfernb(array, buffer, array.size)
      BCM.bcm2835_spi_end
      return buffer
    end
  end

  module_function :write, :read_write
end
