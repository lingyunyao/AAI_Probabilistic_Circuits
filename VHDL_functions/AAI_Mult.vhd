-- This is a AAI Mult VHDL model
-- Initially written by Lingyun Yao
-- Last modification by Lingyun Yao, lingyun.yao@aalto.fi, 30.05.2024
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;

entity ProductNode_Float is
  generic(mantissaBits: integer ; exponentBits: integer );
    port( 
	  vinf1  : in  std_logic_vector(exponentBits+mantissaBits-1 downto 0);
     vinf2  : in  std_logic_vector(exponentBits+mantissaBits-1 downto 0);
   voutf0 : out std_logic_vector(exponentBits+mantissaBits-1 downto 0)
        );
end ProductNode_Float;

architecture rtl of ProductNode_Float is

   
signal bias_mantissa: std_logic_vector (mantissaBits-1 downto 0 ):=(others => '0');
signal bias_all_0: std_logic_vector (exponentBits+mantissaBits-1 downto 0 ):=(others => '0');
signal bias_exp: std_logic_vector (exponentBits-2 downto 0 ):=(others => '1');
signal bias: std_logic_vector (exponentBits+mantissaBits-1 downto 0 ):="0" & bias_exp & bias_mantissa;

begin
voutf0 <=bias_all_0 when (vinf1=bias_all_0 or vinf2=bias_all_0) else vinf1+vinf2-bias;

end rtl;
