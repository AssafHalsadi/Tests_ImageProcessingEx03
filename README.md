# HUJI Image Processing course (67829) Ex3 Tests 2020/2021<a name="TOP"></a>
[![Build Status](https://img.shields.io/badge/build%20version-1.0-green)](https://github.com/AssafHalsadi/Tests_ImageProcessingEx02)
![cover](readme_assets/cover.png)

Testing suite for the third exercise of Image Processing course (67829) at HUJI. The suite includes basic tests for most of the exercises functions that checks the API, the return values, usage of loops and some functionality. In this README I will go over [requirements](#REQ), a [guide](#HOWTO) of how to use the tests, each tests coverage and what it means to pass it.

## TLDR - If you don't know what to do, start here
The table of contents has links to all of the needed instructions, if you are just interested in running the tests:

Go to [Installation](#SETUP), install the tests, and [run the tests](#HOWTO).

If you are confused about the results, go to the [Understanding your results](#UNDER) section.

If you don't know what a test checks, go to the [Test Scopes](#SCOPES) section.

If you find any issues, or want to ask a question, go to the [Contact Info](#CONTACT) section.


## :warning: DISCLAIMER :warning:
Passing these tests DOES NOT guaranty you will get a good grade in any way, as they are not moderated by the course's staff.
I will try and make it as clear as possible as to which extent the tests cover the exercise, but i felt the disclaimer was needed in any case.

**Generally** _(Will be expanded in "Test Scopes" section)_
1. Tests for Pyramid Building related functions check the size is correct for the general pyramid and each level separately and that the value range does not change when creating a gaussian pyramid.
2. The est for recreating the image from laplacian checks that the recreated image is close to the original, working with a cv2 built in implementation (kind of) of a laplacian pyramid. Uses correlation I chose, might induce false positives.
3. Tests the rendering module creates a proper image.
Tests for "blending" were not implemented, as we are required to actually blend images, and if an issue rises, we will see it.

All tests cover basic API checks, correct usage of return/loops and some specific functionality that is explained in the [code doc](#DOC).

## Table Of Contents
* General Info
    * [Documentation](#DOC)
    * [Collaborators](#COL)
    * [Contact Info](#CONTACT)
* How to use
    * [Installation](#SETUP)
    * [Running Through Command Line](#CMD) (Textual Interface)
    * [Running Through Pycharm](#PY)
* Understanding your results
    * [Trough Command Line](#CMD2) (Textual Interface)
    * [Through Pycharm](#PY2)
* Test Scopes
    * DFT Tests
        * ['test_DFT_IDFT_1D'](#1D)
        * ['test_DFT2_IDFT2'](#2D)
    * Audio Speed Tests
        * ['test_change_rate'](#RATE)
        * ['test_resize'](#RESIZE)
        * ['test_change_samples'](#SAMPLES)
        * ['test_resize_spectogram'](#SPECTROGRAM)
        * ['test_resize_vocoder'](#VOCODER)
    * :x: DEPRECATED :x: ~~Derivative Tests~~ 
        * [~~'test_conv_der'~~](#CONVDER)
        * [~~'test_fourier_der'~~](#FOURIERDER)

    
## :books: Documentation<a name="DOC"></a>
[![](https://user-images.githubusercontent.com/4301109/70686099-3855f780-1c79-11ea-8141-899e39459da2.png)](https://assafhalsadi.github.io/Tests_ImageProcessingEx02/. )

:arrow_up: _Easy navigation through this README file can be found here_ :arrow_up:
_images might not work there_

## Collaborators<a name="COL"></a>
[Assaf Halsadi](https://github.com/AssafHalsadi) :israel:

[Ron Moran](https://github.com/ronmoran) :israel:

## Contact Info<a name="CONTACT"></a>
:heavy_exclamation_mark: please do not send me private messages about the tests through whatsapp

If you find any mistakes, or have any questions - please contact me through the course's Slack [![Slack](https://img.shields.io/badge/HUJI_IMPR_20%20slack-join-green?logo=slack&labelColor=4A154B)](https://join.slack.com/t/huji-impr-20/shared_invite/zt-i5z2lgja-vs8c6RptH8t2_jou~Wvhuw)

Or at the courses forum at the relevant post [![forum](https://img.shields.io/badge/moodle%20forum-goto-orange?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAXCAMAAAAm/38fAAABdFBMVEUNDg4ODw8PEA8PEBAQEA8QEBEQEhMREhEREhISEhETEhATEhEUEhAUFBQVFBEWFxcXFBEXFxgZFRAZFREaFhEcFREcHh4hGBIhHh0iISEkGhElHBQlHRglJCUmJCUmJCYnHhUnJCQoHRQoJSMpHhQpJygqHRIqHhUrJCEsHRQtJSEtKSsxIxQxLi8zLCo0MjQ1JBQ2JhU2KyU3MzE3NDU4IhY5IhU5JBQ5KBc9P0E/JhRAKRVBKxVDQEFDQkVEKBlEPDlEPDtJMBpMTE9PKxlQS0tRRD9TLhpUPzBUSEJjWlhmQh9oXlppQyJuRyFwPhlyV0Z2QRp2QRuPUiCPa1OWViKYWCOfXy2qaSmsZSa0bSq1biq6aye8cCi8cyq/bCjBdCvFcCjFcSjHcijLfC3NbifReyvUdCvWeyvZdCnZfivadSnffyvfgivigizreSftiy7viyvwfSnwhCryhi3zfSjzfij1hyv1iSz2jiz2jyz2jy3O+s8EAAAAtUlEQVR42mMY7ICVg5cXQ5BZUFJOUVGWH02YXdnBzVFXW56NS1pBAElcwtPHy9XWRNXINzIjK9abDy4hoyVm6WynrxdeUpGXW1ngB5cQF2XwCAkw1ogvz3GySKuKg0vYmzIEFaWrM4SVJ4twRlelwCXcXRgCy7JVGELLk4Q5o6oREppmDIGlmSCJRCEUCSZuZAmQUQjgn5+qxBBcHCPEGVGYgCwhZWXOw6BmbcDCqGNjOPCxAwBHvSY/OMtgWQAAAABJRU5ErkJggg==&labelColor=4A154B)](https://moodle2.cs.huji.ac.il/nu20/course/view.php?id=67829)

## Requirements<a name="REQ"></a>
To run the tests you will only need the following things:

[![python](https://img.shields.io/badge/python-3-blue.svg?logo=python&labelColor=yellow)](https://www.python.org/downloads/)
[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg?logo=windows)](https://github.com/AssafHalsadi/Tests_ImageProcessingEx02)
[![file](https://img.shields.io/badge/file-sol3.py-red?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAXCAMAAAAm/38fAAABdFBMVEUNDg4ODw8PEA8PEBAQEA8QEBEQEhMREhEREhISEhETEhATEhEUEhAUFBQVFBEWFxcXFBEXFxgZFRAZFREaFhEcFREcHh4hGBIhHh0iISEkGhElHBQlHRglJCUmJCUmJCYnHhUnJCQoHRQoJSMpHhQpJygqHRIqHhUrJCEsHRQtJSEtKSsxIxQxLi8zLCo0MjQ1JBQ2JhU2KyU3MzE3NDU4IhY5IhU5JBQ5KBc9P0E/JhRAKRVBKxVDQEFDQkVEKBlEPDlEPDtJMBpMTE9PKxlQS0tRRD9TLhpUPzBUSEJjWlhmQh9oXlppQyJuRyFwPhlyV0Z2QRp2QRuPUiCPa1OWViKYWCOfXy2qaSmsZSa0bSq1biq6aye8cCi8cyq/bCjBdCvFcCjFcSjHcijLfC3NbifReyvUdCvWeyvZdCnZfivadSnffyvfgivigizreSftiy7viyvwfSnwhCryhi3zfSjzfij1hyv1iSz2jiz2jyz2jy3O+s8EAAAAtUlEQVR42mMY7ICVg5cXQ5BZUFJOUVGWH02YXdnBzVFXW56NS1pBAElcwtPHy9XWRNXINzIjK9abDy4hoyVm6WynrxdeUpGXW1ngB5cQF2XwCAkw1ogvz3GySKuKg0vYmzIEFaWrM4SVJ4twRlelwCXcXRgCy7JVGELLk4Q5o6oREppmDIGlmSCJRCEUCSZuZAmQUQjgn5+qxBBcHCPEGVGYgCwhZWXOw6BmbcDCqGNjOPCxAwBHvSY/OMtgWQAAAABJRU5ErkJggg==)](https://moodle2.cs.huji.ac.il/nu20/course/view.php?id=67829)

## How to - running the tests<a name="HOWTO"></a>
### Setup<a name="SETUP"></a> 
1. Clone this repository into a _"tests"_ folder within your project's root folder:
    * Open a new folder named _"tests"_ in your project's root folder.
    * Open a command line on your computer, I will use cmd as an example on windows:
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/02.png" width="500"></p>
    </details>
    
    * Go to the _tests_ folder using the `cd` command like so : `_cd [path_to_project]/tests` (change [path_to_project] with the path to your project):
     <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/03.png" width="500"></p>
    </details>
    
    * Go to the [top of the page](#TOP), there you should copy the git link: 
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/01.png" width="350"></p>
    </details>
    
    * Type `git clone *copy here*` :
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/04.png" width="500"></p>
    </details>
    
    * You might be prompted to enter your [CSE user credentials](https://wiki.cs.huji.ac.il/wiki/Password_and_OTP#OTP_and_UNIX_passwords)
    
    :x: Step 2 no longer needed :x:
    
~~2. Unpack the _output_compare.rar_ located in the _output_compare_ folder.~~
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/05.png" width="300"></p>
    </details>

 
3. Copy both _sol2.py_, _ex2_helper.py_ and any other files needed for your implementation to the _tests_ folder.
4. At the end your "tests" folder should look like this:
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/11.png" width="300"></p>
    </details> 
   
5. That is it, no need for complicated voodoo. :smile:

### Usage 
There are two main ways to run the tests, via the Textual Interface or via pycharm's built in unittest support.
I'll go through both of these here.
#### Textual Interface<a name="CMD"></a>
1. Go to the project's folder.
2. Go to the _tests_ sub-folder.
3. Double click on _'RunMe.bat'_:
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/06.png" width="300"></p>
    </details>
 
If everything went according to plan, A cmd window should open, and after a while the tests will start running.

**Remark**: Some of the tests take A LOT of time to complete. To run only SOME of the tests open the _runner.py_ and scroll down to this function:
![testList](../readme_assets/07.png)
Flip which lines are commented like so:
![testList02](../readme_assets/08.png)
and delete the names of the tests you don't want to run.
#### Pycharm<a name="PY"></a>
1. Go to _test _ sol2.py_ file, located in the "tests" folder.
2. To run all of the tests, scroll down to the TestSuite start and click the green "play" button :
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/09.png" width="500"></p>
    </details>

3. To run an individual test, scroll down to the test's function and click on the green "play" button beside it :
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/10.png" width="500"></p>
    </details>
You can identify tests by the face they all start with `def test_...`

## Understanding your results<a name="UNDER"></a>
### Through Command Line<a name="CMD2"></a>
Once you open _RunMe.bat_ a command line window will open, and after a short while the tests will start running.
There are 9 tests that cover general test cases for all of the exercise's API (some tests test multiple functions).
 
The testing process will look like this:
<details>
<summary>Open Image</summary>
<p><img src="../readme_assets/12.png" width="500">

* The RED part indicates how many tests are left.
* The GREEN part will only show if that particular test have finished running and either be "ok" if the test passed or "FAILED" otherwise.
* The last test in the list will be the one that is currently running, and will look like the ORANGE part in the image.
* The text in the PURPLE part will be the NAMES of the tests and their location in the code.

</p>
</details>

When the tester ends, if you passed all test you will see the word "OK" in capital letters at the bottom of the window, like so:
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/13.png" width="500"></p>
    </details>

Otherwise, you will see "Failure" at the bottom, and the number of failed tests:
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/17-2.png" width="500"></p>
    </details>

and which tests failed at the top:
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/17-1.png" width="500"></p>
    </details>
    
The errors will be separated by a line of "===", and look like the following picture:
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/18.png" width="1000"></p>
    </details>
    
### Through Pycharm<a name="PY2"></a>
Once you run a test, a console will open at the bottom of the pycharm screen, make sure both of the following symbols are pressed to be able to see all tests, both passed tests and failed ones:
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/15.png" width="500"></p>
    </details>
    
If you passed all of the tests, all branches at the bottom left of the screen will have a small green :heavy_check_mark: and a red "OK" will be written at the bottom of the console:
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/14.png" width="500"></p>
    </details>
    
If you haven't, some tests will have a small orange X mark beside them:
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/16.png" width="500"></p>
    </details>
    
Each error explanation will begin with the word "Failure", followed by the traceback of the issue:
    <details>
    <summary>Open Image</summary>
    <p><img src="../readme_assets/19.png" width="1000"></p>
    </details>

## Test Scopes<a name="SCOPES"></a>
### DFT Tests
All DFT tests compare the output to the built in numpy.fft counterpart functions.
#### 'test_DFT_IDFT_1D'<a name="1D"></a>
```python
"""

Tests both DFT and IDFT functions by comparing them to the built in np.fft.___ functions.
Allows 1.e-5 difference.
:return: -

"""
```
This test tests both the DFT and IDFT functions applied to the _aria _ 4kHz.wav_ file, it covers:
* Checks no loops are used in the implementation.
* Checks the signature is correct.
* Makes sure the shape and type of the output is correct (UPDATE 1.3: Checks the shape wasn't changed from input).
* Compares the output to the 'np.fft.fft' and 'np.fft.ifft' functions, allowing errors of up to 1.e-5 (as the built in implementation is more precise).  

#### 'test_DFT2_IDFT2'<a name="2D"></a>
```python
"""
Tests both DFT2 and IDFT2 functions by comparing them to the built in np.fft.___ functions.
Allows 1.e-5 difference.
:return: -
"""
```
This test tests both the DFT2 and IDFT2 functions applied to the _monkey.jpg_ file in grayscale mode, it covers:
* Checks the signature is correct.
* Makes sure the shape and type of the output is correct (UPDATE 1.3: Checks the shape wasn't changed from input).
* Compares the output to the 'np.fft.fft2' and 'np.fft.ifft2' functions, allowing errors of up to 1.e-5 (as the built in implementation is more precise).  

### Audio Speed Tests
All speed tests check the new speed is correct but not all of them go into HOW the speed was changed.
#### 'test_change_rate'<a name="RATE"></a>
```python
"""
Tests the change rate function by comparing the outputted wav speed to the speed its supposed to be in
and also makes sure the data did not change.
:return: -
"""
```
This test tests the "change_rate" function applied to multiple ratios, it covers:
* Checks the signature is correct.
* Makes sure the function does not return anything.
* Makes sure the wav file data was not changed by the function.
* Checks the new speed of the wav file is correct, allowing errors of up to 1.e-3.  

#### 'test_resize'<a name="RESIZE"></a>
```python
"""
Tests resize function by checking the outputted arrays have the correct length in correspondance to the given
ratio. DOES NOT test how the array was resized.
:return: -
"""
```
This test tests the "resize" function applied to multiple arrays, it covers:
* Checks the signature is correct.
* Makes sure the returned array is 1D.
* Makes sure the returned dtype is correct according to pdf.
* Checks the new size is correct.

:warning: Does not check HOW you resize the array, make sure you follow the pdf :warning:

#### 'test_change_samples'<a name="SAMPLES"></a>
:round_pushpin: This test might take a lot of time to run
```python
"""
Tests the "change_samples" function by using the speed test module.
:return: -
"""
```
This test tests the "change_samples" function applied to multiple ratios, it covers:
* Checks the signature is correct.
* Makes sure the function does not return anything.
* Makes sure the wav file rate was not changed by the function.
* Checks the new speed of the wav file is correct, allowing errors of up to 1.e-3.  

#### 'test_resize_spectrogram'<a name="SPECTROGRAM"></a>
```python
"""                                                                
Tests the "resize_spectrogram" function by using the speed test module.
:return: -                                                         
"""
```
This test tests the "resize_spectrogram" function applied to multiple ratios, it covers:
* Checks the signature is correct.
* Makes sure the wav file rate was not changed by the function.
* Checks the new speed of the wav file is correct, allowing errors of up to 1.e-1 for fast forwarding and 5.e-1 for slowing down.

#### 'test_resize_vocoder'<a name="VOCODER"></a>
```python
"""
Tests the "resize_vocoder" function by using the speed test module.
:return: -
"""
```
This test tests the "resize_vocoder" function applied to multiple ratios, it covers:
* Checks the signature is correct.
* Makes sure the wav file rate was not changed by the function.
* Checks the new speed of the wav file is correct, allowing errors of up to 1.e-1 for fast forwarding and 5.e-1 for slowing down.

# :x: Deprecated tests :x:
### Derivative Tests
All derivative tests compare to MY OUTPUT and might be wrong due to that.
#### ~~'test_conv_der'~~<a name="CONVDER"></a>
```python
"""
Tests the "conv_der" function by using the derivative testing module.
:return: -
"""
```
This test tests the "conv_der" function applied to multiple images, it covers:
* Checks the signature is correct.
* Compares output to MY RESULTS. 

#### ~~'test_fourier_der'~~<a name="FOURIERDER"></a>

:round_pushpin: This test might take a lot of time to run
```python
"""
Tests the "fourier_der" function by using the derivative testing module.
:return: -
"""
```
This test tests the "fourier_der" function applied to multiple images, it covers:
* Checks the signature is correct.
* Compares output to MY RESULTS. 


