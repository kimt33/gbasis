"""Functions for computing overlap of a basis set."""
from gbasis.base_two_symm import BaseTwoIndexSymmetric
from gbasis.contractions import GeneralizedContractionShell
from gbasis.integrals._moment_int import _compute_multipole_moment_integrals
import numpy as np


class Overlap(BaseTwoIndexSymmetric):
    """Class for obtaining the overlap for a set of Gaussian contractions.

    Attributes
    ----------
    _axes_contractions : tuple of tuple of GeneralizedContractionShell
        Sets of contractions associated with each axis of the array.

    Properties
    ----------
    contractions : tuple of GeneralizedContractionShell
        Contractions that are associated with the first and second indices of the array.

    Methods
    -------
    __init__(self, contractions)
        Initialize.
    construct_array_contraction(contractions_one, contractions_two) :
    np.ndarray(M_1, L_cart_1, M_2, L_cart_2)
        Return the overlap associated with a `GeneralizedContractionShell` instance.
        `M_1` is the number of segmented contractions with the same exponents (and angular momentum)
        associated with the first index.
        `L_cart_1` is the number of Cartesian contractions for the given angular momentum associated
        with the first index.
        `M_2` is the number of segmented contractions with the same exponents (and angular momentum)
        associated with the second index.
        `L_cart_2` is the number of Cartesian contractions for the given angular momentum associated
        with the second index.
    construct_array_cartesian(self) : np.ndarray(K_cart, K_cart)
        Return the overlap integrals associated with Cartesian Gaussians.
        `K_cart` is the total number of Cartesian contractions within the instance.
    construct_array_spherical(self) : np.ndarray(K_sph, K_sph)
        Return the overlap integrals associated with spherical Gaussians (atomic orbitals).
        `K_sph` is the total number of spherical contractions within the instance.
    construct_array_mix(self, coord_types, **kwargs) : np.ndarray(K_cont, K_cont)
        Return the overlap integrals associated with the contraction in the given coordinate system.
        `K_cont` is the total number of contractions within the given basis set.
    construct_array_lincomb(self, transform) : np.ndarray(K_orbs, K_orbs)
        Return the overlap integrals associated with the linear combinations of contractions in the
        given coordinate system.
        `K_orbs` is the number of basis functions produced after the linear combinations.

    """

    @staticmethod
    def construct_array_contraction(contractions_one, contractions_two):
        """Return the evaluations of the given contractions at the given coordinates.

        Parameters
        ----------
        contractions_one : GeneralizedContractionShell
            Contracted Cartesian Gaussians (of the same shell) associated with the first index of
            the overlap.
        contractions_two : GeneralizedContractionShell
            Contracted Cartesian Gaussians (of the same shell) associated with the second index of
            the overlap.

        Returns
        -------
        array_contraction : np.ndarray(M_1, L_cart_1, M_2, L_cart_2)
            Overlap associated with the given instances of GeneralizedContractionShell.
            First axis corresponds to the segmented contraction within `contractions_one`. `M_1` is
            the number of segmented contractions with the same exponents (and angular momentum)
            associated with the first index.
            Second axis corresponds to the angular momentum vector of the `contractions_one`.
            `L_cart_1` is the number of Cartesian contractions for the given angular momentum
            associated with the first index.
            Third axis corresponds to the segmented contraction within `contractions_two`. `M_2` is
            the number of segmented contractions with the same exponents (and angular momentum)
            associated with the second index.
            Fourth axis corresponds to the angular momentum vector of the `contractions_two`.
            `L_cart_2` is the number of Cartesian contractions for the given angular momentum
            associated with the second index.

        Raises
        ------
        TypeError
            If contractions_one is not a GeneralizedContractionShell instance.
            If contractions_two is not a GeneralizedContractionShell instance.

        """
        if not isinstance(contractions_one, GeneralizedContractionShell):
            raise TypeError("`contractions_one` must be a GeneralizedContractionShell instance.")
        if not isinstance(contractions_two, GeneralizedContractionShell):
            raise TypeError("`contractions_two` must be a GeneralizedContractionShell instance.")

        coord_a = contractions_one.coord
        angmoms_a = contractions_one.angmom_components_cart
        alphas_a = contractions_one.exps
        coeffs_a = contractions_one.coeffs
        norm_a_prim = contractions_one.norm_prim_cart
        coord_b = contractions_two.coord
        angmoms_b = contractions_two.angmom_components_cart
        alphas_b = contractions_two.exps
        coeffs_b = contractions_two.coeffs
        norm_b_prim = contractions_two.norm_prim_cart
        return _compute_multipole_moment_integrals(
            np.zeros(3),
            np.zeros((1, 3), dtype=int),
            coord_a,
            angmoms_a,
            alphas_a,
            coeffs_a,
            norm_a_prim,
            coord_b,
            angmoms_b,
            alphas_b,
            coeffs_b,
            norm_b_prim,
        )[0]


def overlap_integral(basis, transform=None, coord_type="spherical"):
    """Return overlap integral of the given basis set.

    Parameters
    ----------
    basis : list/tuple of GeneralizedContractionShell
        Shells of generalized contractions.
    transform : np.ndarray(K_orbs, K_cont)
        Transformation matrix from the basis set in the given coordinate system (e.g. AO) to linear
        combinations of contractions (e.g. MO).
        Transformation is applied to the left, i.e. the sum is over the index 1 of `transform`
        and index 0 of the array for contractions.
        Default is no transformation.
    coord_type : {"cartesian", list/tuple of "cartesian" or "spherical", "spherical"}
        Types of the coordinate system for the contractions.
        If "cartesian", then all of the contractions are treated as Cartesian contractions.
        If "spherical", then all of the contractions are treated as spherical contractions.
        If list/tuple, then each entry must be a "cartesian" or "spherical" to specify the
        coordinate type of each GeneralizedContractionShell instance.
        Default value is "spherical".

    Returns
    -------
    array : np.ndarray(K_orbs, K_orbs)
        Overlap integral of the given basis set.
        Dimensions 0 and 1 of the array correspond to the basis functions. `K_orbs` is the number of
        basis functions in the basis set.

    """
    if transform is not None:
        return Overlap(basis).construct_array_lincomb(transform, coord_type)
    if coord_type == "cartesian":
        return Overlap(basis).construct_array_cartesian()
    if coord_type == "spherical":
        return Overlap(basis).construct_array_spherical()
    return Overlap(basis).construct_array_mix(coord_type)
