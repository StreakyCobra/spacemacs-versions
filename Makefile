fakehome/:
	mkdir fakehome
	git clone --recursive https://github.com/syl20bnr/spacemacs fakehome/.emacs.d

clean:
	rm -rf fakehome
